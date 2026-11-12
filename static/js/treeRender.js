class TreeRenderer {
    constructor(svgElementOrId, options = {}){
        this.svg = typeof svgElementOrId === "string"
        ? document.getElementById(svgElementOrId)
        : svgElementOrId

        if(!this.svg) {
            console.error("TreeRender: Invalid SVG element or ID provided.")
        }

        this.options = {
            viewBoxWidth: 1000,
            viewBoxHeight: 550,
            nodeRadius: 22,
            interactive: true,
            onNodeClick: null,
            ...options
        };

        this.nodesMap = new Map();
        this.edgesMap = new Map();
        this.currentTreeData = null;

        this.initSVG();
    }

    initSVG(){
        if (!this.svg) return;
        this.svg.setAttribute("viewBox", `0 0 ${this.options.viewBoxWidth} ${this.options.viewBoxHeight}`);
        this.svg.setAttribute("preserveAspectRadio", "xMidYMid meet");
        this.svg.classList.add("tree-svg");
    }


    // Clear svg canvas
    clear(){
        if(!this.svg) return;
        this.svg.innerHTML = "";
        this.nodesMap.clear();
        this.edgesMap.clear();
        this.currentTreeData = null;
    }

    // Render a tree from JSON data (as return by flask backend)
    render(treeData){
        this.clear();
        if(!treeData || !this.svg) return;

        this.currentTreeData = treeData;

        const edgesLayer = document.createElementNS("http://www.w3.org/2000/svg", "g");
        edgesLayer.setAttribute("class", "tree-edges-layer");

        const nodesLayer = document.createElementNS("http://www.w3.org/2000/svg", "g");
        nodesLayer.setAttribute("class", "tree-edges-layer");

        this.svg.appendChild(edgesLayer);
        this.svg.appendChild(nodesLayer);

        // Pass 1: Flatten nodes to compute pixel coordinates
        const nodesList = [];
        const edgesList = [];

        const traverse = (node, parent = null) => {
            if (!node) return;

            const pxX = (node.x / 100.0) * this.options.viewBoxWidth;
            const pxY = (node.y / 100.0) * this.options.viewBoxHeight;

            const nodeInfo = {
                val: node.val,
                x: pxX,
                y: pxY,
                depth: node.depth,
                data: node
            };
            nodesList.push(nodeInfo);

            if (parent) {
                edgesList.push({
                    parentVal: parent.val,
                    childVal: node.val,
                    x1: parent.x,
                    y1: parent.y,
                    x2: pxX,
                    y2: pxY
                });
            }

            if (node.left) traverse(node.left, nodeInfo);
            if (node.right) traverse(node.right, nodeInfo);
        };

        traverse(treeData);

        // Pass 2: Draw connections lines (Edges)
        edgesList.forEach(edge => {
            const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
            line.setAttribute("x1", edge.x1);
            line.setAttribute("y1", edge.y1);
            line.setAttribute("x2", edge.x2);
            line.setAttribute("y2", edge.y2);
            line.setAttribute("class", "tree-edge");
            line.setAttribute("data-from", edge.parentVal);
            line.setAttribute("data-to", edge.childVal);

            edgesLayer.appendChild(line);
            this.edgesMap.set(`${edge.parentVal}-${edge.childVal}`, line);
        });

        // Pass 3: Draw circles & text lablales (Nodes)
        nodesList.forEach(node => {
            const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
            g.setAttribute("class", "tree-node");
            g.setAttribute("data-val", node.val);
            g.setAttribute("transform", `translate(${node.x}, ${node.y})`);

            // Node circle
            const circle = document.createElementNS("http://www.w3.org/2000/svg","circle");
            circle.setAttribute("r", this.options.nodeRadius);
            circle.setAttribute("class", "tree-node");
            circle.setAttribute("cx", 0);
            circle.setAttribute("cy", 0);

            const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
            text.setAttribute("class", "node-text");
            text.setAttribute("x", 0);
            text.setAttribute("y", 0);
            text.textContent = node.val;
          
            g.appendChild(circle);
            g.appendChild(text);

            if (this.options.interactive){
                g.addEventListener("click", ()=>{
                    if(typeof this.options.onNodeClick === "function"){
                        this.options.onNodeClick(node.val, node);
                    }
                });
            }

            nodesLayer.appendChild(g);
            this.nodesMap.set(node.val, {g, circle, text, nodeInfo: node});
        });
    }


    // Set semantic state of a node: default, active, correct, wrong, solved
    setNodeState(val, state){
        const item = this.nodesMap.get(val);
        if (!item) return;

        item.g.classList.remove("node-active", "node-correct", "node-wrong", "node-solved");

        if (state !== "default"){
            item.g.classList.add(`node-${state}`);
        }
    }

    // Trigger a red error shake animation on a node 
    shakeNode(val){
        const item = this.nodesMap.get(val);
        if (!item) return;

        item.g.classList.remove("node-wrong")
        void item.g.offsetWidth;
        item.g.classList.add("node-wrong");

        setTimeout(() => {
            item.g.classList.remove("node-wrong");
        }, 500);
    }

    resetAllNodes(){
        this.nodesMap.forEach(({g}) => {
            g.classList.remove("node-active", "node-correct", "node-wrong", "node-solved");
        });
        this.resetAllNodes();
    }

    highlightEdge(parentVal, childVal, active=true) {
        const edge = this.edgesMap.get(`${parentVal}-${childVal}`);
        if (edge) {
            if (active) {
                edge.classList.add("edge-active");
            } else {
                edge.classList.remove("edge-active");
            }
        }
    }

    resetAllEdges(){
        this.edgesMap.forEach(line => {
            line.classList.remove("edeg-active");
        });
    }

    highlightPath(nodeValues){
        this.resetAllNodes();
        nodeValues.forEach(val => {
            this.setNodeState(val, "active");
        })
    }
}