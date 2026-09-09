---
layout: default
title: Lab Resources
has_children: false
nav_order: 5
---

# {{page.title}}

## Spare keys

There is a spare key to the 309 office suite. Ask a lab member for access to it.

## Office Supplies

The Yuyan lab keeps office supplies in the lab in 310. They are inside a cabinet along the inside wall with a green label "Office Supplies." There you can find writing utensils, flash drives and other useful tools.

## Technical Support

Contact Bala using the PMACS support email: [psom-pmacshpc@pennmedicine.upenn.edu](psom-pmacshpc@pennmedicine.upenn.edu)


## Our Neighbors in Stellar-Chance

Our most immediate neighbor is [Dr. Katherine Uyhazi](https://www.med.upenn.edu/apps/faculty/index.php/g275/p8763511) in the adjacent lab in 311.

Yuyan also shares her office suite with [Dr. Ahmara Ross](https://www.med.upenn.edu/apps/faculty/index.php/g275/p8837640) and [Dr. Kenneth Schindler](https://www.med.upenn.edu/apps/faculty/index.php/g324/p3888).

We also share our floor with [Dr. Qi N Cui](https://www.med.upenn.edu/apps/faculty/index.php/g275/p8931117), [Dr. Dwight Stambolian](https://www.med.upenn.edu/apps/faculty/index.php/g275/p5715) and, most recently, [Dr. Jeff Sundstrom](https://www.pennmedicine.org/providers/profile/jeffrey-sundstrom).

Lastly, we have the honor of joining the Chair of Opthalmology [Dr. Joshua Dunaief](https://www.med.upenn.edu/apps/faculty/index.php/g275/p6071) on our floor of Stellar-Chance Laboratories.

## This Website

This website is a [github-pages](https://docs.github.com/en/pages) site using [just-the-docs](https://open.win.ox.ac.uk/pages/open-science/community/just-the-docs-v040/) and [jekyll](https://jekyllrb.com/docs/) to get it running.

To modify this site, clone this repository to your computer from the `Source` link in the top right of the webpage. From there, go to the [jekyll site](https://jekyllrb.com/docs/). Follow its quickstart guide to install [Ruby](https://www.ruby-lang.org/en/downloads/) and update the [Ruby Gem](https://rubygems.org/pages/download) system. From there, use Gem on the command line to install Jekyll with `gem install jekyll bundler`.

Still on the command line, go into the cloned repo and run `bundle install`. This will make Jekyll use this repository's Gemfile and Gemfile.lock files to install all of the correct versions of software needed to run the site on your computer. If you get errors, it might be best to delete the local Gemfile.lock before running bundle install. When that is done, run `bundle exec jekyll serve`.

Now go to http://localhost:4000// in your web browser to see this website locally!

From here, you can modify the files in this repository and see your changes at the http://localhost:4000// website in real time as jekyll recompiles your markdown each time your save.

When you are happy with the changes, terminate and restart the `bundle exec jekyll serve` command to make sure the site builds properly on your machine. Then commit and push these changes through git if you are an administrator. If not, either send the content to the administrator through messaging or a git pull request. Do not push your local `Gemfile.lock`. When the main branch is pushed, the website is automatically re-built and re-deployed. It may take up to 10 minutes for changes to appear.

The last step is to ensure that your changes were properly implemented by checking that the website matches what you saw on your machine.
