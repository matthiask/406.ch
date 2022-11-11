import fh_fablib as fl


fl.require("1.0.20221102")
fl.config.update(host="www-data@feinheit06.nine.ch")
fl.config.update(domain="406.ch", branch="master", remote="production")

ns = fl.Collection(*fl.GENERAL, *fl.NINE)
