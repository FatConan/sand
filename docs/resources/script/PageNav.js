import "jquery";
import _ from "underscore";

//ElementHelper taken from the Malic-Acid project at https://github.com/FatConan/malic-acid
class ElementHelper{
    static guid(){
        function s4() {
            return Math.floor((1 + Math.random()) * 0x10000)
                .toString(16)
                .substring(1);
        }
        return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
            s4() + '-' + s4() + s4() + s4();
    }

    static getData(element, dataLabel){
        if(element !== null){
            return $(element).data(dataLabel);
        }
        return null;
    }

    /**
     * Legacy alias for findParentByTag
     * @param element
     * @param tagName
     */
    static findParentTag(element, tagName){
        return ElementHelper.findParentByTag(element, tagName);
    }

    /**
     * Find the first element tracking up the provided element's branch that matches the provided tag string
     * @param element
     * @param tagName
     * @returns {*}
     */
    static findParentByTag(element, tagName){
        while(element && element.tagName !== tagName.toUpperCase() && element.tagName !== null){
            element = element.parentNode;
        }
        return element;
    }

    /**
     * Find the first element tracking up the provided element's branch that matches the provided string
     * @param element
     * @param match
     * @returns {null|{matches}|*}
     */
    static findParentByMatch(element, match){
        while(element && element.tagName !== null){
            if(element.matches){
                if(element.matches(match)){
                    return element;
                }
            }
            element = element.parentNode;
        }
        return null;
    }

    /**
     * This method is used when registering events and is used internally to track up from the target element to
     * see if we catch an match and element in its branch. We wil then return that element and any registered event actions
     * associated with it
     * @param element - A DOM element
     * @param matchObj - An event handler object
     * @returns {*[][]|({matches}|*|string)[]}
     */
    static parentMatches(element, matchObj){
        while(element && element.tagName !== null){
            if(element.matches){
                for(let m in matchObj){
                    if(matchObj.hasOwnProperty(m) && element.matches(m)){
                        return [element, m, matchObj[m]];
                    }
                }
            }
            element = element.parentNode;
        }
        return [null, null, []];
    }

    static match(element, matchStr){
        if(element && element.matches){
            return element.matches(matchStr);
        }
        return false;
    }

    static matches(element, matchObj){
        if(element && element.matches){
            for(let m in matchObj){
                if(matchObj.hasOwnProperty(m) && element.matches(m)){
                    return [element, m, matchObj[m]];
                }
            }
        }
        return [null, null, []];
    }

    //Methods for performing quick sort on objects, allows sorting on various items based on a given key
    static swap(items, firstIndex, secondIndex){
        let temp = items[firstIndex];
        items[firstIndex] = items[secondIndex];
        items[secondIndex] = temp;
    }

    static partition(items, itemKey, left, right){
        let pivot = items[Math.floor((right + left) / 2)][itemKey];
        let i = left;
        let j = right;

        while(i <= j){
            while(items[i][itemKey] < pivot){
                i++;
            }

            while(items[j][itemKey] > pivot){
                j--;
            }

            if(i <= j){
                ElementHelper.swap(items, i, j);
                i++;
                j--;
            }
        }
        return i;
    }

    static quickSort(items, itemKey, left, right){
        let index;
        if(items.length > 1){
            left = typeof left !== "number" ? 0 : left;
            right = typeof right !== "number" ? items.length-1 : right;
            index = this.partition(items, itemKey, left, right);
            if(left < index-1){
                ElementHelper.quickSort(items, itemKey, left, index-1);
            }
            if(index < right){
                ElementHelper.quickSort(items, itemKey, index, right);
            }
        }
        return items;
    }
}

//HighLevelEventHanlder taken from the Malic-Acid project at https://github.com/FatConan/malic-acid
class HighLevelEventHandler{
    /** The HighLevelEventHandler is a touch/click event tracker that registers once at document level as a single listener
     * for intercepting click events. It also resolved events against their intended target so that an event firing on a child
     * element but listened for at an ancestor can provide the listener with that intended ancestor to work with automatically.
     * @param options An object of configuration options:
     *  {
     *      touchscreen: true/false, //Determines whether we listen for click events or touch events
     *      loadingWarning: function //Which function to trigger in the event it appears that an unhandled anchor is being clicked.
     *  }
     */

    constructor(options){
        this.elementHelper = ElementHelper;
        this.listenerGroupName = options.groupName;
        this.touchscreen = options.touchscreen === true;
        this.debug = false;
        this.nullAction = function(e){
        };

        //We can specify in the options a loadWarning to function to fire on the event that we hit a link that looks
        //like it should have a javascript action associated with it (a link with <a href="#">) to indicator to the
        //developer that it looks like we have an unregistered event.

        //Should we actually want to a link to link to # (such as a top of page link) we can specify a null listener on that
        //element.
        if(options.loadingWarning){
            this.loadingWarning = options.loadingWarning;
        }else{
            this.loadingWarning = function(){
                alert("Not quite ready! The page is currently loading and this function isn't quite read yet, please try again.");
            };
        }

        this.target = $(options.target);
        this.listeners = {};
        this.listenerPluginGroups = {};
        if(!options.groupName){
            this.listen();
        }
    }

    static hookup(options){
        if(!window.eventHandler){
            window.eventHandler = new this(options);
        }
    }

    static grabHandler(){
        if(window.eventHandler){
            return window.eventHandler;
        }
        throw "HighLevelEventHandler has not been instantiated, or is not present at the expected location. Instantiate the " +
        " handler by calling HighLevelEventHandler.hookup({options})";
    }

    addListenerGroup(groupName){
        let newGroupListener = new HighLevelEventHandler({groupName: groupName, touchscreen: this.touchscreen});
        this.listenerPluginGroups[groupName] = newGroupListener;
        return newGroupListener;
    }

    removeListenerGroup(groupName){
        delete this.listenerPluginGroups[groupName];
    }

    //Add a listener for a specific element and a corresponding action to take
    addListener(targetMatch, action){
        if(this.listeners[targetMatch]){
            this.listeners[targetMatch].push(action);
        }else{
            this.listeners[targetMatch] = [action];
        }
    }

    //Add a null listener. This will suppress any load warnings while not altering behavior.
    addNullListener(targetMatch){
        /* Add a null listener, used to allow elements within elements to invoke default behaviour when their parent has a listener present */
        this.addListener(targetMatch, this.nullAction);
    }

    //Show debug messaging about registered events when they fire
    enableDebug(){
        this.debug = true;
    }

    //List all the currently registered events for debug purposes
    list(){
        const listListeners = function(listenerObj){
            for(let a in listenerObj){
                if(listenerObj.hasOwnProperty(a)){
                    console.log(a,listenerObj[a]);
                }
            }
        }

        console.log("Base Listeners:");
        listListeners(this.listeners);
        for(let g in this.listenerPluginGroups){
            if(this.listenerPluginGroups.hasOwnProperty(g)){
                console.log(`Plugin Listeners [${g}]:`);
                listListeners(this.listenerPluginGroups[g].listeners);
            }
        }
    }

    report(listenerTarget){
        if(this.listeners.hasOwnProperty(listenerTarget)){
            console.log(listenerTarget, this.listeners[listenerTarget])
        }else{
            console.log(`No event listeners found for ${listenerTarget}`);
        }
    }

    clearListeners(listenerTarget){
        if(this.listeners.hasOwnProperty(listenerTarget)){
            delete this.listeners[listenerTarget];
        }
    }

    //Listens for events and the top level and performs any DOM traversal required to accommodate the listener's intended
    //target.
    listen(){
        /* We sometimes hit the scenario where not all of the events for a page have been registered. This means any
        javascript trigger links that have been marked up like <a href="#">Thing</a> cause the page to jump to the top.
        We can remove the href, but then they'd just do nothing instead. This listener, if triggered on such a link,
         prevents the default action of the event, then goes through its even list looking for a match.
         If it fails to find one to match said link then it pops up a "Sorry this isn't loaded yet" message prompting the user
         to try again (but it's really more of a guide to the dev that they've missed something).
         */

        //Determine which event type we should be listening for and make some style adjustments in the case we're operating
        //on a touchscreen
        this.clickEvent = "click";
        if(this.touchscreen && "ontouchstart" in document.documentElement){
            this.clickEvent = "touchstart";
            //Disable the cursor on touchscreens
            $("html").css("cursor", "none");
        }

        // Register the event on out intended top level target (this may be at the top, or on some specific container section within the DOM)
        this.target.on(this.clickEvent, function(e){
            if(this.debug){
                console.log("HIGH LEVEL EVENT HANDLER firing on ", e);
            }
            const el = e.target;
            const $el = $(el);

            /*
                Check to see if we're looking at a link with a "#" href, in which case we know we're dealing with a
                link that's supposed to trigger a javascript event; Stop them making the page jump if nothing is loaded.
             */
            let simpleTopLink = false;
            if($el.attr("href") === "#"){
                if(this.debug){
                    console.log("HIGH LEVEL EVENT HANDLER suppressing default for empty link ", e);
                }
                e.preventDefault();
                simpleTopLink = true;
            }

            let activeListeners = _.extend({}, this.listeners);
            for(let group in this.listenerPluginGroups){
                if(this.listenerPluginGroups.hasOwnProperty(group)){
                    activeListeners = _.extend(activeListeners, this.listenerPluginGroups[group].listeners);
                }
            }

            //From the trigger element work up through the dom until we find an matching event handler, if we find a match return it
            // as well as the list of actions associated with it.
            let match = this.elementHelper.parentMatches(el, activeListeners);
            if(match !== null && match[0] !== null){
                /*
                  Check to see if we have a match in the listener list for the object being clicked by tracking up through the
                  DOM until we find a match. Harvest the details of those matching elements and pass them alongside the original event to
                  the registered action function.
               */
                $(match[2]).each(function(i, action){
                    if(this.debug){
                        console.log("HIGH LEVEL EVENT HANDLER performing actions for ", match, e);
                    }
                    //execute the action. Listeners registered with this system should expect two arguments (a, args)
                    //the first being the original event, the second being a collection of pre-prepared elements containing
                    //the original e.target element and its jquery extended version as well as the matched element and
                    //its jquery extended version and the string user to match the element.
                    action(e, {el: el, $el: $el, matchedEl: match[0], $matchedEl: $(match[0]), trigger: match[1]});
                }.bind(this));
            }else if(simpleTopLink){
                /*
                    If we don't find a match, but the clicked element is a link with an href of "#" assume something else is supposed to be catching it that
                    hasn't been loaded yet (this highLevelHandler should load first, so check if there are events registered on the element) in which case just inform people that the page is still loading.
                 */
                if(this.debug){
                    console.log("HIGH LEVEL EVENT HANDLER showing not loaded message on simple link ", e);
                }
                const ev = $._data(el, 'events');
                if(!ev || !ev.click){
                    this.loadingWarning();
                }
            }else if(this.debug){
                /* Otherwise do nothing (or log we're doing nothing) */
                console.log("HIGH LEVEL EVENT HANDLER taking no further action ", e);
            }
        }.bind(this));
    }
}

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
        //Hookup the event listener.
        HighLevelEventHandler.hookup({
            touchscreen: false, //Determines whether we listen for click events or touch events
            loadingWarning: function(){},
            target: "html"
        });

        //Create a sand listener group
        this.e = HighLevelEventHandler.grabHandler().addListenerGroup("sand");
        //And listen to it
        this.e.listen();
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
        menu.append("<button class=\"close-menu\">Close Navigation</button>")
        this.descendTree(this.target.children(), null, nodes);
        this.descendMenu(menu, nodes);
        this.menuElement.empty().append(menu);
    }

    addListeners() {
        this.e.addListener("#navigator", function(){
            let show = this.menuElement.hasClass("inactive");
            if(show){
                this.menuElement.removeClass("inactive");
            }else{
                this.menuElement.addClass("inactive");
            }
        }.bind(this));
        this.e.addListener("button.close-menu", function(){
             this.menuElement.addClass("inactive");
        }.bind(this));
        this.e.addListener(".main-navigation a", function(){
             this.menuElement.addClass("inactive");
        }.bind(this));
    }
}

window.onload = function(){
    new PageNavigator();
}