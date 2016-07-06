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
require('rxjs/add/operator/toPromise'); //for toPromise()
//import { IMAGES } from '../mock-images';
var http_1 = require("@angular/http");
var Rx_1 = require("rxjs/Rx");
var ImageService = (function () {
    function ImageService(http) {
        this.http = http;
        this.imagesUrl = 'app/images.json';
    }
    ImageService.prototype.getImages = function () {
        //return Promise.resolve(IMAGES);
        //return IMAGES;
        return this.http.get(this.imagesUrl)
            .toPromise()
            .then(function (response) { return response.json(); }) //.data)
            .catch(this.handleError);
    };
    ImageService.prototype.getImage = function (id) {
        return this.getImages()
            .then(function (images) { return images.filter(function (image) { return image._id === id; })[0]; });
        //return this.getImages().filter(image => image.id === id)[0];
    };
    // getImagesSlow (){
    //    return  new Promise<Image[]>(resolve => setTimeout(() => resolve(IMAGES), 4000));
    // }
    ImageService.prototype.extractData = function (res) {
        var body = res.json();
        console.log(body);
        return body || {};
    };
    ImageService.prototype.handleError = function (error) {
        // In a real world app, we might use a remote logging infrastructure
        // We'd also dig deeper into the error to get a better message
        var errMsg = (error.message) ? error.message : error.status ? error.status + " - " + error.statusText : 'Server error';
        console.error(errMsg); // log to console instead
        return Rx_1.Observable.throw(errMsg);
    };
    ImageService = __decorate([
        core_1.Injectable(), 
        __metadata('design:paramtypes', [http_1.Http])
    ], ImageService);
    return ImageService;
}());
exports.ImageService = ImageService;
//# sourceMappingURL=image.service.js.map