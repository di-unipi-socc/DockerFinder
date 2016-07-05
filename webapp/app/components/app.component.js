/**
 * Created by dido on 7/5/16.
 */
"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var core_1 = require('@angular/core');
// Add the RxJS Observable operators we need in this app.
require('../rxjs-operators');
var image_detail_component_1 = require('./image-detail.component');
var AppComponent = (function () {
    function AppComponent() {
        this.images = IMAGES;
    }
    //constructor( private imageService: ImageService)
    AppComponent.prototype.onSelect = function (image) {
        this.selectedImage = image;
    };
    AppComponent = __decorate([
        core_1.Component({
            selector: 'my-app',
            template: "\n    <h1>DoFinder Images</h1>\n    <ul class=\"images\">\n        <li *ngFor=\"let image of images\"  [class.selected]=\"image === selectedImage\" (click)=\"onSelect(image)\"> \n           <span class=\"badge\"> {{image.id}}</span> {{image.name}}\n        </li>\n    </ul>\n    \n    <my-image-detail [image]=\"selectedImage\"></my-image-detail>\n   \n    <!--image-list></image-list-->\n  ",
            styles: ["\n      .selected {\n        background-color: #CFD8DC !important;\n        color: white;\n      }\n      .images {\n        margin: 0 0 2em 0;\n        list-style-type: none;\n        padding: 0;\n        width: 15em;\n      }\n      .images li {\n        cursor: pointer;\n        position: relative;\n        left: 0;\n        background-color: #EEE;\n        margin: .5em;\n        padding: .3em 0;\n        height: 1.6em;\n        border-radius: 4px;\n      }\n      .images li.selected:hover {\n        background-color: #BBD8DC !important;\n        color: white;\n      }\n      .images li:hover {\n        color: #607D8B;\n        background-color: #DDD;\n        left: .1em;\n      }\n      .images .text {\n        position: relative;\n        top: -3px;\n      }\n      .images .badge {\n        display: inline-block;\n        font-size: small;\n        color: white;\n        padding: 0.8em 0.7em 0 0.7em;\n        background-color: #607D8B;\n        line-height: 1em;\n        position: relative;\n        left: -1px;\n        top: -4px;\n        height: 1.8em;\n        margin-right: .8em;\n        border-radius: 4px 0 0 4px;\n      }\n    "],
            directives: [
                image_detail_component_1.ImageDetailComponent
            ]
        }), 
        __metadata('design:paramtypes', [])
    ], AppComponent);
    return AppComponent;
}());
exports.AppComponent = AppComponent;
var IMAGES = [
    { id: 11, name: 'java' },
    { id: 12, name: 'dido' },
    { id: 13, name: 'Bombasto' },
    { id: 14, name: 'Celeritas' },
    { id: 15, name: 'Magneta' },
    { id: 16, name: 'RubberMan' },
    { id: 17, name: 'Dynama' },
    { id: 18, name: 'Dr IQ' },
    { id: 19, name: 'Magma' },
    { id: 20, name: 'Tornado' }
];
//# sourceMappingURL=app.component.js.map