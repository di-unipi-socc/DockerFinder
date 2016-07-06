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
 * Created by dido on 7/5/16.
 */
var core_1 = require('@angular/core');
var mock_images_1 = require('../mock-images');
var ImageService = (function () {
    function ImageService() {
        this.imagesUrl = 'api/images'; // URL to web API
    }
    ImageService.prototype.getImages = function () {
        return Promise.resolve(mock_images_1.IMAGES);
        //return IMAGES;
        // return this.http.get(this.imagesUrl)
        //                 .map(this.extractData)
        //                 .catch(this.handleError);
    };
    ImageService.prototype.getImage = function (id) {
        return this.getImages()
            .then(function (images) { return images.filter(function (image) { return image.id === id; })[0]; });
        //   return this.getImages().filter(image => image.id === id)[0];
    };
    ImageService.prototype.getImagesSlow = function () {
        return new Promise(function (resolve) { return setTimeout(function () { return resolve(mock_images_1.IMAGES); }, 4000); }); //resolbe iamges after 4 seconds
        // return this.http.get(this.imagesUrl)
        //                 .map(this.extractData)
        //                 .catch(this.handleError);
    };
    ImageService = __decorate([
        core_1.Injectable(), 
        __metadata('design:paramtypes', [])
    ], ImageService);
    return ImageService;
}());
exports.ImageService = ImageService;
//# sourceMappingURL=image.service.js.map