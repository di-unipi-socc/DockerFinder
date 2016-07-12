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
/**
 * Created by dido on 7/10/16.
 */
var core_1 = require('@angular/core');
var image_service_1 = require('../services/image.service');
var images_component_1 = require('../components/images.component');
var router_1 = require("@angular/router");
var ImagesSearchComponent = (function () {
    function ImagesSearchComponent(router, imageService) {
        this.router = router;
        this.imageService = imageService;
        this.submitted = false;
        this.sorting = ['stars', 'pulls',];
        this.ordering = ['ascending order', 'descending order'];
        this.count = 0;
    }
    ImagesSearchComponent.prototype.onSubmit = function () {
        var _this = this;
        this.imageService.searchImages(this.diagnostic)
            .then(function (images) {
            if (images.length > 0) {
                _this.resultImages = images;
                _this.count = images.length;
                console.log(images);
            }
        }); //res in the json
        this.submitted = true;
        //this.router.navigate(['/images']);
    };
    Object.defineProperty(ImagesSearchComponent.prototype, "diagnostic", {
        // TODO: Remove this when we're done
        get: function () { return this.bin + "=" + this.version; },
        enumerable: true,
        configurable: true
    });
    ImagesSearchComponent.prototype.edit = function () {
        this.submitted = false;
        this.resultImages = [];
    };
    ImagesSearchComponent = __decorate([
        core_1.Component({
            selector: 'my-search-images',
            templateUrl: 'app/template/images-search.component.html',
            directives: [images_component_1.ImagesComponent]
        }), 
        __metadata('design:paramtypes', [router_1.Router, image_service_1.ImageService])
    ], ImagesSearchComponent);
    return ImagesSearchComponent;
}());
exports.ImagesSearchComponent = ImagesSearchComponent;
// class SearchUrlEncoded{
//     bins = [{bin:String, ver:String}];
//
// }
//# sourceMappingURL=images-search.component.js.map