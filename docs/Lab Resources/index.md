---
layout: default
title: Lab Resources
has_children: false
nav_order: 5
---

# {{page.title}}

## Penn Resources in General

## Spare keys

## The office supplies

## Technical Support

## Our Neighbors in Stellar-Chance

## This Website

This website is a [github-pages](https://docs.github.com/en/pages) site using [just-the-docs](https://open.win.ox.ac.uk/pages/open-science/community/just-the-docs-v040/) and [jekyll](https://jekyllrb.com/docs/) to get it running.

To modify this site, clone this repository to your computer from the `Source` link in the top right of the webpage. From there, go to the [jekyll site](https://jekyllrb.com/docs/). Follow its quickstart guide to install [Ruby](https://www.ruby-lang.org/en/downloads/) and update the [Ruby Gem](https://rubygems.org/pages/download) system. From there, use Gem on the command line to install Jekyll with `gem install jekyll bundler`.

Still on the command line, go into the cloned repo and run `bundle install`. This will make Jekyll use this repository's Gemfile and Gemfile.lock files to install all of the correct versions of software needed to run the site on your computer. When that is done, run `bundle exec jekyll serve` and go to http://localhost:4000// in your web browser to see this website with your local changes.

From there, you can modify the files in this repository and see your changes at the http://localhost:4000// website.

When you are happy with the changes, terminate and restart the `bundle exec jekyll serve` command to make sure the site builds properly on your machine. Then commit and push these changes through git. When the main branch is pushed, the website is automatically re-built and re-deployed. It may take up to 10 minutes for changes to appear.

The last step is to ensure that your changes were properly implemented by checking that the website matches what you saw on your machine.

### Operations

Theme, pages, organization, etc
