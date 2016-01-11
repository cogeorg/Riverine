<script type="text/javascript">
    modelData = {{modelData|tojson|safe}};
    conf_obj = {{conf_obj|tojson|safe}};
    headers = {{headers|tojson|safe}};
    var _kernel = "gaussian";


    

    var i;
    
    var margin ={bottom:40, top:20, left:50, right:30};
    //var margin = {top:20, right:30, bottom: 40, left:50};
    var width = 600-(margin.left+margin.right);
    var height = 400-(margin.top+margin.bottom);

    var svg = d3.select("#svg_kde")
            .attr("width", width+margin.left+margin.right)
            .attr("height", height+margin.top+margin.bottom)
          .append("g")
            .attr("transform", "translate("+margin.left+","+margin.top+")");
    
    var _data = _kde.formatData(modelData, headers);

    var bandwidth = new Array;

    for (i=0; i<headers.length; ++i){
        //Create an input type dynamically.
        var element = document.createElement("input");
        
        //Create Labels
        var label = document.createElement("Label");
        label.innerHTML = headers[i] + ": ";     
        
        var bw = 1.06*d3.deviation(_data[i])*Math.pow(_data[i].length,-1.0/5.0);
        bandwidth.push( bw );
        
        //Assign different attributes to the element.
        element.setAttribute("type", "text");
        element.setAttribute("value", bw.toString());
        element.setAttribute("name", "txt_bandwidth"+ i.toString());
        element.setAttribute("style", "width:200px");
        
        label.setAttribute("style", "font-weight:normal");
        
        var div_bandwidth = document.getElementById("div_bandwidth");
        
        //Append the element in page (in span).
        div_bandwidth.appendChild(label);
        div_bandwidth.appendChild(element);
    }

    var xlabel =  conf_obj["model"]["visualizer"]["xlabel"]["@value"];   
    var ylabel =  conf_obj["model"]["visualizer"]["ylabel"]["@value"];   

    _kde.draw(_data, bandwidth, _kernel, headers, svg, margin, width, height, xlabel, ylabel)


    // Build Visualization function for user interaction with model data
    function BuildVisualization(){   
        var i;
        for (i=0; i<bandwidth.length; ++i){
            bandwidth[i] = $("input:text[name=txt_bandwidth"+ i.toString()+"]").val(); 
        }
        console.log(bandwidth)
        svg.selectAll("*").remove();
        svg = d3.select("#svg_kde")
            .attr("width", width+margin.left+margin.right)
            .attr("height", height+margin.top+margin.bottom)
          .append("g")
            .attr("transform", "translate("+margin.left+","+margin.top+")");
        _kernel = $("#kernel option:selected").val(); 
        _kde.draw(_data, bandwidth, _kernel, headers, svg, margin, width, height, xlabel, ylabel)         
    }

</script>
