<script type="text/javascript" src="static/js/topojson.js"></script>
 
<script type="text/javascript">
    modelData = {{modelData|tojson|safe}};
    conf_obj = {{conf_obj|tojson|safe}};
    coords = {{coords|tojson|safe}};
    categories = {{categories|tojson|safe}};
    
    id_index = 0;
    _min = Math.round(categories[id_index]["min"]);
    _max = Math.round(categories[id_index]["max"]);
    
    visualization = d3plus.viz();
    
    function make_viz(_visualization, _data){
        //visualization = d3plus.viz()
        _visualization.container("#viz"); // container DIV to hold the visualization
        _visualization.type("geo_map") // visualization type
        //.title({"value": categories[id_index]["label"], "position": "top"});
    
        _visualization.data(_data); // data to use with the visualization
        _visualization.id("code") // key for which our data is unique on
        _visualization.color(categories[id_index]["key"]);
        _visualization.tooltip(categories[id_index]["key"]);
    
        _visualization.text("country") // key to use for display text
        _visualization.coords(coords)
    
        _visualization.height(500) 	//set the height (in pixels) of the current output -default is 600
        _visualization.width(700)
        _visualization.legend({"value":true, "size":20, "icons":true})
        _visualization.draw() // render the visualization!
    }
    
    function refresh_viz(_visualization, _data){
    
        _visualization.data(_data); // data to use with the visualization
        _visualization.id("code"); // key for which our data is unique on
        _visualization.color(categories[id_index]["key"]);
        _visualization.tooltip(categories[id_index]["key"]);
    
        _visualization.text("country"); // key to use for display text
        _visualization.coords(coords);
    
        _visualization.draw(); // render the visualization!
    }
    
    function filter_data(_data, _key, range){
        //console.log("Filtering " + _key + " for range " + range.min + " to " + range.max);

        if (range.min <= _min && range.max >= _max)
            return _data;

        filtered_data = new Array;
        for (var i=0; i<_data.length; ++i){
            if ( _data[i][_key] >= range.min && _data[i][_key] <= range.max ){
                filtered_data.push(_data[i])
            }
        }
        return filtered_data;
    }
</script>
