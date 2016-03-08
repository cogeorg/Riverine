<script>
    modelData = {{modelData|tojson|safe}};
    conf_obj = {{conf_obj|tojson|safe}};
    focus = {{focus|tojson|safe}};

    visualization = d3plus.viz();

    function init_visualization(){
        visualization.container("#ring_viz")
        visualization.type("rings") 
    

        // Size and color nodes by value 'size'
        /* Doesn't show second neighbors for some reason        
        visualization.data(modelData.nodes)
        visualization.id("node_id")
        visualization.size("size")
        visualization.color("size")
        */

        // Size edges by value 'strength'
        visualization.edges({
          "size": "strength",
          "value": modelData.edges
        })

        visualization.height(700)
        visualization.width(1000)
        visualization.focus(focus)
        visualization.draw() 
    }

</script>
