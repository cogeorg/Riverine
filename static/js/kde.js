!function(){
    _kde = {};

    kernels = ["epanechnikov", "gaussian", "uniform", "cosine", "logistic"];

    //Epanechnikov kernel
    function Epanechnikov(bandwidth){
    	var alpha = 0.75/bandwidth;
    	return function(u){
    		u /= bandwidth;
    		return (Math.abs(u)<= 1.0? alpha*(1-u*u):0);
    	};
    }
    
    //Gaussian kernel
    function Gaussian(bandwidth){
    	var alpha = 1/(Math.sqrt(2*Math.PI)*bandwidth);
    	return function(u){
    		u/=bandwidth;
    		return alpha*Math.exp(-.5*u*u);
    	};
    }
    
    //Uniform kernel
    function Uniform(bandwidth){
    	var alpha = .5/bandwidth;
    	return function(u){
    		u /= bandwidth;
    		return Math.abs(u)<=1.0?alpha:0;
    	};
    }
    
    //Cosine kernel
    function Cosine(bandwidth){
    	var alpha = Math.PI/(4*bandwidth);
    	var beta = Math.PI/2;
    	return function(u){
    		u /= bandwidth;
    		return Math.abs(u)<=1.0?alpha*Math.cos(beta*u):0;
    	};
    }
    
    //Logistic kernel
    function Logistic(bandwidth){
    	var alpha = 1/bandwidth;
    	return function(u){
    		u/= bandwidth;
    		return alpha/(Math.exp(u)+2+Math.exp(-u));
    	};
    }
    
    //Kernel Density Estimator function
    function KernelDensityEstimator(_x, _kernel){
    	//var _kernel = Epanechnikov(_bandwidth);
    	return{	
    		update: function(_newKernel){
    			_kernel = _newKernel;
    		},
    	
    		compute: function(sample){
    			var pdf = [];
    			var i, j, _y;
    			var n = sample.length;
    			for (i=0; i<_x.length; ++i){
    				_y = 0;
    				for (j=0; j<sample.length; ++j){
    					_y += _kernel(_x[i]-sample[j]);
    				}
    				pdf.push([_x[i],_y/n]);
    			}
    			return pdf;
    		}
    	};
    }

    function getKernel(_kernel, bandwidth){
        switch(_kernel){
            case "epanechnikov":
                return Epanechnikov(bandwidth);
                break;
            case "gaussian":
                return Gaussian(bandwidth);
                break;
            case "uniform":
                return Uniform(bandwidth);
            case "cosine":
                return Cosine(bandwidth);
            case "logistic":
                return Logistic(bandwidth);
                break;
            default:
                return Guassian(bandwidth);
                break;
        }
    }

    _kde.formatData = function(data, headers){
        _data = new Object;
        var i,j;
        for (i=0; i<headers.length; ++i){
            _data[i] = new Array;
            for (j=0; j<data.length; ++j){
                _data[i][j] = data[j][i];
            }
        }
        return _data;
    }

    _kde.draw = function(_data, bandwidth, _kernel, headers, svg, margin, width, height, xlabel, ylabel){

        if (bandwidth.length != headers.length)
            return;
        var i, keys = new Array, _tmp;
        var _minX, _maxX, _maxY, stub;

        _minX = d3.min(_data[0])
        _maxX = d3.max(_data[0])

        for (i=0; i<headers.length; ++i){
            keys.push(i);
            _stub = d3.extent(_data[i]);
            if (_stub[0]<_minX)
                _minX = _stub[0];
            if (_stub[1]>_maxX)
                _maxX = _stub[1];
        }

        var xScale = d3.scale.linear()
        	.domain([_minX-0.1*_maxX, 1.4*_maxX])
        	.range([0, width]);

        var kde = KernelDensityEstimator(xScale.ticks(200), getKernel(_kernel,bandwidth[0]));	

        var kde_data = new Object;

        _maxY = 0;

        for (i=0; i<headers.length; ++i){
            //bandwidth = 1.06*d3.deviation(_data[i])*Math.pow(_data[i].length,-1.0/5.0);
            kde.update(getKernel(_kernel,bandwidth[i]));
            kde_data[i] = kde.compute(_data[i]);
    
            _stub = d3.max(kde_data[i], function(d){return d[1];})
            if (_stub > _maxY ){
                _maxY = _stub;
            }
        }

        if (_maxY>=.9)
            _maxY = 1;
        else if (_maxY>=.8)
            _maxY = .9;
        else if (_maxY>=.7)
            _maxY = .8;
        else if (_maxY>=.6)
            _maxY = .7;
        else if (_maxY>=.5)
            _maxY = .6;
        else if (_maxY>=.4)
            _maxY = .5;
        else if (_maxY>=.3)
            _maxY = .4;
        else if (_maxY>=.2)
            _maxY = .3;
        else if (_maxY>=.1)
            _maxY = .2;
        else
            _maxY = .1;
            	
        var yScale = d3.scale.linear()
        	.domain([0, _maxY])
        	.range([height, 0]);
        	
        var xAxis = d3.svg.axis()
        	.scale(xScale)
        	.orient("bottom");
        
        var yAxis = d3.svg.axis()
        	.scale(yScale)
        	.orient("left")
        	.tickFormat(d3.format("%"))

        var line = d3.svg.line()
           .interpolate("basis")
           .x(function(d){return xScale(d[0]);})
        	.y(function(d){return yScale(d[1]);});	

        var colors = d3.scale.category10()
            .domain(keys);

        for (i=0; i<headers.length; ++i){                    
            svg.append("path")
            	.datum(kde_data[i])
            	.attr("class", "line")	
            	.attr("d", line)
            	.attr("data-legend", headers[i])
            	.attr("data-legend-color", colors(i))
                 .style("opacity", ".5")
                 .style("stroke", colors(i));
        }
        			
        svg.append("g")
        	.attr("class", "x axis")
        	.attr("transform", "translate(0,"+height+")")
        	.call(xAxis)
          .append("text")
          	.attr("class", "label")
          	.attr("x", width)	
          	.attr("y", -6)
          	.style("text-anchor", "end")
          	.text(xlabel);	

        svg.append("g")
        	.attr("class", "y axis")	
        	.call(yAxis)
           .append("text")
        	   .attr("transform", "rotate(-90)")
        	   .attr("y", 6)
        	   .attr("dy", ".71em")
        	   .style("text-anchor", "end")
        	   .style("font-size", "10px")
        	   .text(ylabel);	

        legend = svg.append("g")
        	.attr("class", "legend")
        	.attr("transform", "translate("+(width-100)+",0)")
        	.style("font-size", "10px")
        	.call(d3.legend);
    }
}();