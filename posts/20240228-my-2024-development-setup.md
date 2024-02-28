Title: My 2024 Development Setup
Date: 2024-02-28
Categories: Programming

# My 2024 Development Setup

I have been inspired by [Jeff Triplett's post](https://micro.webology.dev/2024/02/18/my-development-setup.html) to write this down. The main value -- if there's value at all in this post -- lies in my ability to revisit it later and see if anything changed.

## Desk

I'm using a standing desk since 2015 or 2016. I'm actually doing most of my work standing; when I'm tired or maybe after a sports session I sit down, but when I do that I mostly choose the sofa or a different table and get back to the standing desk as soon as possible. I have started using the standing desk when I was in therapy for severe back pain but I have come to like it a lot since then. I do have a chair but I don't really use it all that often.

The greatest thing about a standing desk is that when I go to an event which involves a lot of standing around (or dancing!) I don't get tired as fast as before :-)

## Hardware

My main machines are two Thinkpad notebooks, a Lenovo X1 carbon and a Lenovo X1 nano. I bought the latter because my previous notebook broke during a warranty repair by a technician and I really really had to have a notebook for the coming days and I already had ordered the former, but it wasn't to be delivered for several weeks. That was annoying. The good thing about it is that I normally do not have to carry around anything when going to the office, since I leave one of them in the office most of the time. I'm using a 27" WQHD monitor when I work. I have used a 32" 4k monitor for some time, but I have noticed that I'm starting to spend time searching for windows. I don't like curved or widescreens monitors at all (I have tried them). I thought I'd never reach the point when I would reduce the available screen size voluntarily, but here I am.

I also have a desktop machine at home, but I mostly use it for gaming, and only a little development on the side. It has a 11th gen i7, 32 GB ram and a GeForce RTX 30 series graphics card.

This also means that I'm switching computers all the time, and basically everything has to be synced to the cloud all the time. I'm using git since the spring of 2006 and push everything all the time anyway. And when I'm not, I'm mostly using web-based software. This means that I mostly don't care about backing up my data, I let the cloud companies and the NSA do it.

## Software

After many years on macOS and a few years on Windows with WSL I am back to using Linux without a VM. I am using Fedora because I actually like the unmodified GNOME 3, and because I prefer flatpaks to snaps. RPM/DNF are alright, but I'm still more accustomed to DEB/APT.

I have left macOS because of the touch bar and the terrible keyboard, and Windows because I don't want ads everywhere on *my* computer.

## Development

I use a terminal emulator (gnome-terminal on Linux, [alacritty](https://alacritty.org/) on Windows/WSL) to run [tmux](https://github.com/tmux/tmux/), and start everything I need directly in there.

I have tried escaping vim many times but have always failed. (No, not *exiting* vim, thanks for your help.) The various VIM modes in popular editors such as VisualStudio Code just do not cut it. I'm currently editing code in [neovim](https://neovim.io/) with a few plugins. The only really important plugin is [ctrlp.vim](https://github.com/ctrlpvim/ctrlp.vim). Ctrl-P with fuzzy matching is a great way to open files. I like vi, and I tell people that I use it when I'm asked but I do not suggest to people that they should use it as well. The learning curve isn't worth it except maybe if you do a lot of system administration, I don't know.

I have a VisualStudio Code installation laying around for using Live Share. I think it's a great way for helping others solve a particular problem in a project they are working on, much better than screen sharing and probably even better than sitting at a table together, just because having two keyboards and cursors is so nice.

I mostly only use virtualenvs created using `python3 -m venv venv` for local development, no containers or anything. I definitely see the value of containers for deployment but I haven't yet gotten around to setting things up for local development. This means that my machine always (also) runs a PostgreSQL and a redis server and maybe some other tools. Python 3 upgrades are mostly painless. NodeJS upgrades have sometimes been painful, but I avoid most of the pain by upgrading relatively late.
