<script type="text/javascript">

org_modelData = {{modelData|tojson|safe}};
conf_obj = {{conf_obj|tojson|safe}};

visualization = d3plus.viz();

//get visualization parameters from the xml model config files
_xaxis = get_param("xaxis");
_yaxis = get_param("yaxis");
_id = get_param("ID");

_min = Number(d3.min(org_modelData, function(d) { return d.value; }));
_max = Number(d3.max(org_modelData, function(d) { return d.value; }));

//The get_param function retrieves the "_param_value" configuration from conf_obj
//The argument _param_value = "xaxis" or "yaxis" or "ID"
function get_param(_param_value){
    var param = new Object;
    var Parameters = conf_obj["model"]["data"]["parameters"]["param"];
    for ( i in Parameters ){
        if(Parameters[i]["@value"].toLowerCase() == _param_value.toLowerCase()){
            param.id = Parameters[i]["@id"]
            param.label = Parameters[i]["@label"]
        }
    }    
    return param;
}
</script>
