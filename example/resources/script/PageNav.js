import "jquery";
import _ from "underscore";

export class PageNavigatorNode {
    constructor($element, depth) {
        this.id = $element.prop("id");
        this.href = $element.prop("href");
        this.$el = $element;
        this.label = $element.text();
        this.clazz = "";
        this.parent = null;
        this.depth = depth;
        this.children = [];
    }

    setClazz(clazz){
        this.clazz = clazz;
    }

    setParent(parent) {
        this.parent = parent;
    }

    addChild(child) {
        this.children.push(child);
    }

    popToDepth(depth) {
        if (this.depth >= depth) {
            if (this.parent !== null) {
                return this.parent.popToDepth(depth);
            }
            return null;
        } else {
            return this;
        }
    }
}


export default class PageNavigator{
    constructor() {
        console.log("PAGE NAVIGATOR CREATED");
        this.navElement = $("#navigator");
        this.menuElement = $("#navigator-menu-container");
        this.target = $("#wrapper");
        this.menuItemTemplate = _.template(`<li <% if(clazz){ %>class="<%- clazz %>"<% } %>><a href="<% if(href){ %><%- href %><% } else{ %>#<%- id %><% } %>"><%- label %></a></li>`);
        this.searchElememnts = ["h1", "h2", "h3", "h4", "h5", "h6"];
        this.buildSkeleton();
        this.addListeners();
    }

    packageElement(element, parent) {
        let depth = this.getDepth(element[0]);
        let el = new PageNavigatorNode(element, depth);
        let correctedParent = this.getCorrectParent(el, parent);
        el.setParent(correctedParent);

        if (correctedParent !== null) {
            correctedParent.addChild(el);
        }

        return el;
    }

    getDepth(element) {
        return parseInt(element.tagName.replace("H", ""), 10);
    }

    getCorrectParent(packedEl, currentEl) {
        if (currentEl !== null) {
            return currentEl.popToDepth(packedEl.depth);
        }
        return null;
    }

    descendTree(childNodes, currentEl, nodes) {
        for (let childNode of childNodes) {
            let $child = $(childNode);

            if (this.searchElememnts.includes(childNode.tagName.toLowerCase())) {
                let pack = this.packageElement($child, currentEl);
                currentEl = pack;
                if (pack.parent === null) {
                    nodes.push(pack);
                }
            }

            this.descendTree($child.children(), currentEl, nodes);
        }
    }

    descendMenu($root, children) {
        let $ul = $("<ul></ul>");
        $root.append($ul);
        for (let child of children) {
            let $li = $(this.menuItemTemplate(child));
            $ul.append($li);
            if (child.children) {
                this.descendMenu($li, child.children);
            }
        }
    }

    buildSkeleton() {
        let nodes = [];
        let menu = $("<div></div>");
        this.descendTree(this.target.children(), null, nodes);
        this.descendMenu(menu, nodes);
        this.menuElement.empty().append(menu);
    }

    addListeners() {
        this.navElement.on("click", function(){
            let show = this.menuElement.hasClass("inactive");
            if(show){
                this.menuElement.removeClass("inactive");
            }else{
                this.menuElement.addClass("inactive");
            }
        }.bind(this));
    }
}

window.onload = function(){
    new PageNavigator();
}