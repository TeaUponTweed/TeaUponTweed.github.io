import glob
import os
import re
import sys
from dataclasses import dataclass
from typing import Dict

import click
import markdown2
import yaml


def extract_front_matter(markdown_text):
    front_matter = None
    content = markdown_text

    match = re.match(r"^---\n(.*?)\n---\n(.*)$", markdown_text, re.DOTALL)

    if match:
        front_matter_str, content = match.groups()
        front_matter = yaml.safe_load(front_matter_str)

    return front_matter, content


@dataclass
class Post:
    name: str
    title: str
    html: str
    date: str


def load_post(post_path: str, header_html: str) -> Post:
    with open(post_path, "r") as fo:
        front_matter, content = extract_front_matter(fo.read())
    post_html = markdown2.markdown(content)

    date = front_matter["date"]
    title = front_matter["title"]
    doc_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">

    <title>{title}</title>

    <link rel="stylesheet" href="style.css">
    <meta name="Author" content="Michael Mason" />
    <meta name="rating" content="SAFE FOR KIDS" />
    <meta name="description" content="{description}" />
    <meta name="keywords" content="{keywords}" />
    <meta name="Classification" content="Blog" />
    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
    <meta name="Language" content="en-US" />
</head>
<body>
{header}
<main>
<article>
    {body}
</article>
</main>
</body>
</html>
""".format(
        title=front_matter["title"],
        header=header_html,
        body=post_html,
        description=front_matter["description"],
        keywords=front_matter["keywords"],
    )
    post_name = os.path.basename(post_path).replace(".md", ".html")
    return Post(
        name=post_name,
        html=doc_html,
        title=title,
        date=date,
    )


@click.command()
@click.option("-p", "postdir", type=str)
@click.option("-o", "outdir", type=str)
def main(postdir: str, outdir: str):
    # header for all files
    header_html = """
    <header>
      <h1>
        <a href="/">MBM Blog</a>
      </h1>
      <nav>
        <a href="/">Posts</a>
        <a href="/static/rss.xml" type="application/rss+xml">Feed</a>
      </nav>
    </header>
"""
    # load posts and convert to HTML
    posts_paths = sorted(glob.glob(os.path.join(postdir, "*.md")), reverse=True)
    posts = [
        load_post(post_path=posts_path, header_html=header_html)
        for posts_path in posts_paths
        if "/Draft_" not in posts_path
    ]
    posts = sorted(
        posts,
        key=lambda x: x.date,
        reverse=True,
    )
    # save posts
    for post in posts:
        with open(os.path.join(outdir, post.name), "w") as fo:
            print(post.html, file=fo)
    # main entrypoint
    index_html = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    
    <title>M. B. Mason's Blog</title>
    <meta name="M. B. Mason's Blog" content="M. B. Mason's Blog">
    
    <!-- Recommended minimum -->
    <title>M. B. Mason's Blog - Programming and Miscellaneous Thoughts</title>
    <meta name="description" content="M. B. Mason's blog on programming and other miscellaneous thoughts, including discussions on various topics such as Nic Cage movies, recipes, and more.">
    <meta property="og:title" content="M. B. Mason's Blog - Programming and Miscellaneous Thoughts">
    <meta property="og:description" content="M. B. Mason's blog on programming and other miscellaneous thoughts, including discussions on various topics such as Nic Cage movies, recipes, and more.">

    <link rel="stylesheet" href="style.css">
    <meta name="keywords" content="nic cage, nicholas cage, blog, michael mason, denver tech blog, michael mason blog, programming, recipes">
    <meta name="Author" content="Michael Mason">
    <meta name="rating" content="SAFE FOR KIDS">
    <meta name="Classification" content="Blog">
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <meta name="copyright" content="Michael Mason">
    <meta name="Language" content="en-US">
  </head>
  <body>
    {header}
    <main>
    <article>
      <ul>
      {body}
      <ul>
    </article>
  </body>
</html>
""".format(
        header=header_html,
        body="\n".join(
            f'<li><a href="/static/{post.name}"> {post.title} </a> </li>'
            for post in posts
        ),
    )
    print(index_html, file=open(os.path.join(outdir, "index.html"), "w"))
    # RSS feed
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
            f"        <item> <title>{post.title}</title> <link>https://blog.derivativeworks.co/static/{post.name}</link> <pubDate>{format_date_for_rss(post.date)}</pubDate> </item>"
            for post in posts
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
