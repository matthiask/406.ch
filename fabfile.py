import fh_fablib as fl


fl.require("1.0.20230303")
fl.config.update(host="www-data@feinheit06.nine.ch")
fl.config.update(domain="406.ch", branch="main", remote="production")

ns = fl.Collection(*fl.GENERAL, *fl.NINE)
