<script>
    modelData = {{modelData|tojson|safe}};
    conf_obj = {{conf_obj|tojson|safe}};
    categories = {{categories|tojson|safe}};
    
    visualization = d3plus.viz();
    searchNode_dropdown = d3plus.form();

    function init_searchNode_dropdown(){
        searchNode_dropdown.container("#search_viz");
        searchNode_dropdown.data(modelData.nodes);
        searchNode_dropdown.id("node_id")
        searchNode_dropdown.text("label")
        searchNode_dropdown.title({"value":"View node:",
            "font": {"align": "right", "color":"#0000ff"}});
        searchNode_dropdown.type("drop");
        searchNode_dropdown.width(150);
        searchNode_dropdown.search(true); 
        searchNode_dropdown.focus(modelData.nodes[0]["node_id"], zoomIntoNode);
        searchNode_dropdown.draw();
    }
    
    function init_visualization(){
        visualization.container("#network_viz")
        visualization.type("network") 
    
        visualization.data(modelData.nodes); 
        visualization.id("node_id")  
        visualization.size("size")
        console.log(modelData)
        visualization.nodes(modelData.nodes);
        visualization.edges({
          "arrows": 0,
          "value": modelData.edges
        })
        
        visualization.height(500)
        visualization.width(700)
        visualization.draw() 
    }
    
    function zoomIntoNode(node){
        visualization.focus({"value": node})
                     .draw();
    }

    function refresh_viz(_visualization, filtered, selection){
        _visualization.id({"value": "node_id", "solo": selection.nodes});
        _visualization.data(filtered.nodes);
        _visualization.size("size")

        var val = new Object;
        val.arrows = 0; 
        if ($('input[name="edge_weights"]:checked').val() == "true"){   
            val.size = "strength";   
            val.label = "strength"    
        } else {
            val.arrows = 0;
        } 
        val.value = filtered.edges;

        _visualization.edges(val);  
        _visualization.draw(); // render the visualization!

        searchNode_dropdown.data(filtered.nodes);
        //searchNode_dropdown.focus(false);
        searchNode_dropdown.draw();
    }
    
    function _eval(selection,edge){
        return(( selection.edges.indexOf(edge["type"]) >= 0 ) 
                    && ( selection.nodes.indexOf(edge["source"].toString()) >= 0 )  
                    && ( selection.nodes.indexOf(edge["target"].toString()) >= 0 ) 
                    && ( edge["strength"] >= selection.edgeRange.min 
                       && edge["strength"] <= selection.edgeRange.max) 
                );
    }

    function filter_data(selection){

        toggle_edgeWeights = $('input[name="edge_weights"]:checked').val();        
        
        filtered = new Object;
        filtered.nodes = new Array;
        filtered.edges = new Array;

        if (selection.nodes != null){
            for (var i=0; i<modelData.nodes.length; ++i){
                if ( selection.nodes.indexOf(modelData.nodes[i]["node_id"]) >= 0 ){
                    filtered.nodes.push(modelData.nodes[i]);                
                }
            }
        }

        org_edges = {{modelData['edges']|tojson|safe}};
        
        if (selection.edges != null){
            for (var i=0; i<org_edges.length; ++i){
                res = _eval(selection, org_edges[i]);
                if (res){                    
                    stub = org_edges[i];
                    if (toggle_edgeWeights=="false"){  
                        stub["strength"] = 0;                             
                    }
                    filtered.edges.push(stub);                
                }
            }
        }
        
        return filtered;
    }
    
    // The following function gets the range (min,max) from data
    // Typical use = range_edges
    function getRange(data, key){
        var range = new Object;
        range.min = Number(d3.min(data, function(d) { return d[key]; }));
        range.max = Number(d3.max(data, function(d) { return d[key]; }));
        return range;
    }
</script>
