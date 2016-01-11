<script type="text/javascript">
    modelData = {{modelData|tojson|safe}};
    conf_obj = {{conf_obj|tojson|safe}};
    headers = {{headers|tojson|safe}};
    param_keys = {{param_keys|tojson|safe}};
  
    var margin ={bottom:40, top:20, left:50, right:30};
    //var margin = {top:20, right:30, bottom: 40, left:50};
    var width = 600-(margin.left+margin.right);
    var height = 400-(margin.top+margin.bottom);

    var svg = d3.select("#svg_scatter")
            .attr("width", width+margin.left+margin.right)
            .attr("height", height+margin.top+margin.bottom)
          .append("g")
            .attr("transform", "translate("+margin.left+","+margin.top+")");
    
    var xlabel =  conf_obj["model"]["visualizer"]["xlabel"]["@value"];   
    var ylabel =  conf_obj["model"]["visualizer"]["ylabel"]["@value"];   

    _scatterplot.draw(modelData, headers, svg, margin, width, height, xlabel, ylabel)
</script>
