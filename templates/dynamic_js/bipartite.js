<script>
    modelData = {{modelData|tojson|safe}};
    conf_obj = {{conf_obj|tojson|safe}};
    headers = {{headers|tojson|safe}};
    data_id = {{data_id|tojson|safe}};
    
    var width = 1200;
    var height = 1200;
    var margin = {b: 0, t: 50, l: 470, r: 50};
    
    var svg_bipartite = d3.select("#svg_bipartite")
        .append("svg:svg")
        .attr('width', width)
        .attr('height', (height + margin.b + margin.t))
        .append("g")
        .attr("transform", "translate(" + margin.l + "," + margin.t + ")");
    
    var data = [ {data:bP.partData(modelData,data_id['column']),
        id:data_id['id'], header:headers} ];
    bP.draw(data, svg_bipartite);
</script>
