import fh_fablib as fl


@fl.task
def deploy(ctx):
    fl.run_local(ctx, "venv/bin/python generate.py")
    fl.run_local(
        ctx, "rsync -avzhP --delete out/ www-data@feinheit06.nine.ch:406.ch/htdocs/"
    )
