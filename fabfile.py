import fh_fablib as fl


fl.require("1.0.20210506")
fl.config.update(base=fl.Path(__file__).parent, host="www-data@feinheit06.nine.ch")
fl.config.update(app="app", domain="406.ch", branch="master", remote="production")

ns = fl.Collection(*fl.GENERAL, *fl.NINE)
