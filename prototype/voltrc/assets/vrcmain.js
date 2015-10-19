
// Classes
function serverinstance() {
   this.id = 0;
   this.state = 0;
   this.timestamp = 0;
   this.ip = "";
   this.port = "";
}
function dbinstance() {
   this.serverlist = "";
   this.deployment = {};
   this.action = "create";
   this.availableactions = "create,recover,add,rejoin";
   this.servers = new Array();
}

var db = new dbinstance();

var current_state = 0;

function get_state() {
//ADD_DEBUG("Get state -- servers=" + db.servers.length + " serverlist=" + db.serverlist);
   if (db.servers.length > 0) {
   		leadserver = db.serverlist.split(",")[0];
   		for (var i=0; i< db.servers.length; i++) {
   			if (db.servers[i].ip == leadserver) {
   				//ADD_DEBUG("Current state (from " + i + ") is " + db.servers[i].state);
   				return db.servers[i].state;
   			}
  		 } 
ADD_DEBUG("Can't find lead node. Use [0] state=" + db.servers[0].state);
    				return db.servers[0].state;
   
  	}
	return 0;
 }
function getserveraddress(server) {
   var addr = server.ip;
   if (server.port != "") addr += ":" + server.port;
   return addr;
 }


//*****************                 *********************
//*****************   UI ACTIONS    *********************

function initUI() {
		//  Get server host name and/or address, port
		var ip = location.host;
		var port = location.port;
		var i = location.host.indexOf(":");
		if (i > -1) ip = ip.substring(0,i);
		db.serverlist = ip;
		
		ADD_DEBUG ("[" + ip + "] : [" + port + "]");
		var data = '{"ip":"' + ip + '"}';
		getREST("GET","init",data,init_callback,badREST, location.host);
		// Start timer
		setInterval(function(){ping_servers();},3000);

}

function start_button() {
	var state = get_state();
	if (state == 0 || state == 3) {
		var opt = document.getElementById("dbaction").innerHTML;
		current_state = 1;
			// Change icon
		change_button("starting");
		//var target = document.getElementById("starttarget").innerHTML;
		// This is completely bogus!
		target='{"id":1}';
		for (var i = 0; i < db.servers.length; i++) {
			getREST("GET",opt,target,start_callback,badREST, getserveraddress(db.servers[i]));
		}
		//alert ("START Action: " + opt);
		return false;
    } else {
       ADD_DEBUG("Current state is " + state);
    }
    
}
function add_server_button() {
	var state = get_state();
	if (state == 0 || state == 3) {
		ADD_DEBUG("add a server");
		$("#addserverModal").modal({"show":"true"});
		return false;
    } else {
      error_box("Cannot add a server while database is running...");
      return(false);
    }
}

function add_server_confirm() {
		ADD_DEBUG("add a server / confirm");
		var ip = document.getElementById("addserverip").value;
		var port = document.getElementById("addserverport").value;
				ADD_DEBUG ("[" + ip + "] : [" + port + "]");
		var data = '{"ip":"' + ip + '"}';
		getREST("GET","init",data,init_callback,badREST, ip + ":" + port);

		return false;
}

function ping_servers() {
   for (var i=0; i<db.servers.length; i++) {
   		getREST("GET","ping","",ping_callback, badREST,getserveraddress(db.servers[i]));
   	 }
}

//*****************    DATA LOADING     *********************
//*****************      ROUTINES      *********************

function load_server_info(o) {
  ADD_DEBUG("Loading server info: " + JSON.stringify(o));
  var s = new serverinstance();
  s.id = o['id'];
  s.state = o['status'];
  s.ip = o['ip'];
  s.port = o['port'];
  s.timestamp = o['timestamp'];

  
  if (db.servers.length == 0) {
     db.servers.push(s);
     // Load other info
     //current_state = s.state;
      load_db_info(o['data']);
  }
  else {
       db.servers.push(s);
  }
  
  // Finally, update the UI
  update_server_ui();
  //update_startbutton_ui();


}
function update_server(o) {
   for (var i=0; i<db.servers.length; i++) {
		if (db.servers[i].ip == o["ip"]) {
			var s = db.servers[i];
			s.state = o["status"];
			s.timestamp = o["timestamp"];
			if (o["msg"] != "") {
				error_box( s["ip"] + ": " + o["msg"]);
			}
		}
   	 }
}


function load_db_info(d) {
	// load deployment, server list
	if (d["serverlist"]) {
		if (d["serverlist"] != "") {
			ADD_DEBUG("Loading DB server list from first server: " + d["serverlist"]);
			db.serverlist = d['serverlist'];
		}
	}
}

function update_server_ui() {
   var l = document.getElementById("serverlist");
   var t = "<ul>";
   // list servers
   for (var i=0; i < db.servers.length; i++) {
   		t = t + "<li>" + db.servers[i].ip + "</li>";
   }
   t = t + "</ul>";
   
   // Add "add" button
   t = t + '<p style="margin:1em;text-align:center;">' +
        '<span  onclick="add_server_button();" class="fa fa-plus-square addserverbutton"></span></p>';
   l.innerHTML = t;
	
}
function update_deployment_ui() {
	// list config

}
function update_action_ui() {
	// list actions

}
function update_startbutton_ui() {
ADD_DEBUG("CHANGE START BUTTON: " + get_state());
 	// based on status, update button
 	switch(get_state()) {
 	   case 0:	// new
		change_button("ready");
 	   	break;
 	   case 1:   // Starting
		change_button("starting");
 	   	break;
 	   case 2:	// runnning
		change_button("running");
 	    break;
 	   case 3:  //stopped
		change_button("stopped");
		break;
 	   case 4:  //unknown
		change_button("unknown");
 	   	break;
 	   default:
 	  
 	}

}


//*****************                *********************
//*****************   CALLBACKS    *********************

function init_callback(object) {
    // Announce it
    //alert("In init callback...");
    goodREST(object);

    //alert("Now check status...")
    ADD_DEBUG("Return status: " + object['status'] + " (type: " + typeof(object['status']) + ")");

    // Check status and report error
    if (object['status'] < 0) {
    	error_box("Cannot access server. " + object['msg']);
    	return;
    }
    
    if ( db.servers.length >  0  && (object['status'] == 1 ||  object['status'] == 2)) {
    	error_box("Cannot add server. Server is already running a database.");
    	return;
    } 
    
    load_server_info(object);
    	//
    
}
function start_callback(object) {
    // ADD_DEBUG("refreshing databases!");
    // Announce it
    goodREST(object);
    // Need some assumptions about results.
    // Plan on:
    // status:
    //      code:
    //      message:
    // data:
    //      status
    //      ...
    
}

function ping_callback(object) {
    // ADD_DEBUG("refreshing databases!");
    // Announce it
    goodREST(object);
    // Need some assumptions about results.
    // Plan on:
    // status:
    //      code:
    //      message:
    // data:
    //      status
    //      ...
    if (object['status'] != get_state() ) {
    	ADD_DEBUG("Ping state change: " + object['status'] + " , " + get_state());
    	update_server(object);
    	update_startbutton_ui(object);
    }
    
}

function change_button(t) {
	var button = document.getElementById("startbutton");

  if (t == "starting") button.innerHTML = '<span class="fa fa-spinner fa-spin spinbutton"></span>';
  if (t == "ready") button.innerHTML = '<span class="fa fa-play-circle playbutton"></span>';
  if (t == "unknown") button.innerHTML = '<span class="fa fa-play-circle playbutton"></span>';
  if (t == "running") button.innerHTML = '<span class="fa fa-check-circle runbutton"></span>';
  if (t == "stopped") button.innerHTML = '<span class="fa fa-play-circle playbutton"></span>';
  change_status_label(t);
  change_nextsteps_label(t);
}
function change_status_label(t) {
	var button = document.getElementById("statuslabel");
  button.innerHTML = t;


}
function change_nextsteps_label(t) {
	var button = document.getElementById("nextsteps");
  if (t == "running") {
  		button.innerHTML = 'Go to <a href="http://' +
  			db.servers[0].ip + ':8080/">Management Center</a>';
	} else {
  		button.innerHTML = "";
   }

}


function refresh_button(object) {
  //ADD_DEBUG("Refresh " + object);
  if (object == "db") {
    getREST("GET","databases","",refresh_db, badREST);
  }
  if (object == "config") {
    getREST("GET","deployments","",refresh_config, badREST);

  }
  if (object == "servers") {
    getREST("GET","servers","",refresh_servers, badREST);

  }

}

function error_box(t) { 
	document.getElementById("errorbox").innerHTML = htmlEncode(t);
}

var msgs = new Array();

function ADD_DEBUG(txt) {
  var dbg = document.getElementById("debugger");
  if (msgs.length > 5) msgs.splice(0,1);
  msgs.push(htmlEncode(txt));
  //alert("Msgs length: " + msgs.length);
  dbg.innerHTML = msgs.join("<br/>");
}
function START_DEBUG(txt) {
    ADD_DEBUG(txt);
    return;
  var dbg = document.getElementById("debugger");
  dbg.innerHTML = "<p>" + htmlEncode(txt) + "</p>";
}

function toggle_visible(id) {
  var o = document.getElementById(id);
  if (o.style.display == 'none') {
      o.style.display = 'block';
  } else {
      o.style.display = 'none';
  }
}
