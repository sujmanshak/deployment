
var configMap = {
  voltroot: { 
	type: "string",
	id: "cfg_targetdir"
  },
  sitesperhost: { 
	type: "number",
	id: "cfg_siteperhost"
  },
  kfactor: { 
	type: "number",
	id: "cfg_ksafety"
  },


  httpport: { 
	type: "number",
	id: "cfg_port_http" 
  },
  adminport: { 
	type: "number",
	id: "cfg_port_admin"
  }

};

var dbMap = {
  name: { 
	type: "string",
	id: "cfg_dbname"
  },


  port: { 
	type: "number",
	id: "cfg_port_client"
  },
  internalport: { 
	type: "number",
	id: "cfg_port_internal"
  },
  jmxport: { 
	type: "number",
	id: "cfg_port_jmx"
  },
  logport: { 
	type: "number",
	id: "cfg_port_log"
  },
  zookeeperport: { 
	type: "number", 
	id: "cfg_port_zk"
  }

};
