<script>
    modelData = {{modelData|tojson|safe}};
    conf_obj = {{conf_obj|tojson|safe}};
    headers = {{headers|tojson|safe}};
    
    var margin = {bottom: 40, top: 20, left: 50, right: 30};
    var width = 600 - (margin.left + margin.right);
    var height = 400 - (margin.top + margin.bottom);

    var svg = d3.select("#svg_histogram")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    
    var _data = _histogram.formatData(modelData, headers);

    var xlabel =  conf_obj["model"]["visualizer"]["xlabel"]["@value"];   
    var ylabel =  conf_obj["model"]["visualizer"]["ylabel"]["@value"];   

    _histogram.draw(_data, headers, svg, margin, width, height, xlabel, ylabel)
</script>
