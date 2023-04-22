import glob
import os
import sys
import re

import markdown2
import click

@click.command()
@click.option('-p', 'postdir', type=str)
@click.option('-o', 'outdir', type=str)
def main(postdir: str, outdir: str):
    posts = sorted(glob.glob(os.path.join(postdir, "*.md")), reverse=True)
    posts = [post for post in posts if "/Draft_" not in post]
    print(posts)
    compiled_posts = {}
    header_html = """
    <header>
      <h1>
        <a href="/#home">MBM Blog</a>
      </h1>
      <nav>
        <a href="/#home">Posts</a>
        <!-- <a href="/#about">About</a> -->
        <a href="/static/rss.xml" type="application/rss+xml">Feed</a>
      </nav>
    </header>
"""
    regex = r".*/[0-9]{8}[\w_]+\.md"
    pattern = re.compile(regex)
    for post in posts:
        assert pattern.match(post) is not None, post


        post_html = markdown2.markdown_path(post)
        date = os.path.basename(post)[:8]
        title = os.path.basename(post)[8:-3].replace("_", " ")
        doc_html = """
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width,initial-scale=1">

        <title>{title}</title>

        <link rel="stylesheet" href="/static/style.css">
        <meta name="Author" content="Michael Mason" />
        <meta name="rating" content="SAFE FOR KIDS" />
        <meta name="Classification" content="Blog" />
        <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
        <meta name="Language" content="en-US" />
    </head>
    <body>
    {header}
    <main>
        {body}
    </main>
    </body>
</html>
""".format(
            title=title, header=header_html, body=post_html
        )
        post_name = os.path.basename(post)[9:].replace('.md', '.html')
        compiled_post = os.path.join(outdir,post_name)
        print(doc_html, file=open(compiled_post, "w"))
        compiled_posts[title, date] = compiled_post

    index_html = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    
    <title>M. B. Mason's Blog</title>
    <meta name="M. B. Mason's Blog" content="M. B. Mason's Blog">
    
    <!-- Recommended minimum -->
    <meta property="og:title" content="M. B. Mason's Blog">
    <meta property="og:description" content="M. B. Mason's blog on programming and other miscellaneous thoughts">
    
    <link rel="stylesheet" href="/static/style.css">
    <meta name="keywords" content="nic cage, nicholas cage, blog, michael mason, denver tech blog, michael mason blog"/>
    <meta name="Author" content="Michael Mason" />
    <meta name="rating" content="SAFE FOR KIDS" />
    <meta name="Classification" content="Blog" />
    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
    <meta name="copyright" content="Michael Mason" />
    <meta name="Language" content="en-US" />
  </head>
  <body>
    {header}
    <main>
    <section id="home"> <!-- HOME -->
      <ul>
      {body}
      <ul>
    </section>
  </body>
</html>
""".format(
        header=header_html,
        body="\n".join(
            f'<li><a href="/{post}"> {title} </a> </li>'
            for (title, date), post in compiled_posts.items()
        ),
    )
    print(index_html, file=open(os.path.join(outdir, "index.html"), "w"))

    rss_html = """
<rss version="2.0">
    <channel>
        <title>M. B. Mason's Blog</title> 
        <link>https://blog.derivativeworks.co</link>
        <description>M. B. Mason's blog on programming and other miscellaneous thoughts</description>
        <language>en-us</language>
{}
    </channel>
</rss>
""".format(
        "\n".join(
            f"        <item> <title>{title}</title> <link>https://blog.derivativeworks.co/{post}</link> <pubDate>{format_date_for_rss(date)}</pubDate> </item>"
            for (title, date), post in compiled_posts.items()
        )
    )
    print(rss_html, file=open(os.path.join(outdir, "rss.xml"), "w"))


def format_date_for_rss(date: str) -> str:
    YYYY = date[:4]
    MM = date[4:6]
    DD = date[6:8]
    months = {
        "01": "Jan",
        "02": "Feb",
        "03": "Mar",
        "04": "Apr",
        "05": "May",
        "06": "Jun",
        "07": "Jul",
        "08": "Aug",
        "09": "Sep",
        "10": "Oct",
        "11": "Nov",
        "12": "Dec",
    }
    return f"{DD} {months[MM]} {YYYY} 12:00:00 MST"


if __name__ == "__main__":
    main()
