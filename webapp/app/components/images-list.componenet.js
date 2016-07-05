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
var image_service_1 = require('../services/image.service');
var ImagesListComponent = (function () {
    function ImagesListComponent(imageService) {
        this.imageService = imageService;
    }
    ImagesListComponent.prototype.ngOnInit = function () {
        this.getImages();
    };
    ImagesListComponent.prototype.getImages = function () {
        var _this = this;
        this.imageService.getImages()
            .subscribe(function (images) { return _this.images = images; }, function (error) { return _this.errorMessage = error; });
    };
    ImagesListComponent = __decorate([
        core_1.Component({
            selector: 'image-list',
            template: "\n    <h1>Tour of Heroes ({{mode}})</h1>\n        <h3>Heroes:</h3>\n        <ul>\n          <li *ngFor=\"let image of images\">\n            {{image.repo_name}}\n          </li>\n        </ul>\n        New hero name:\n        \n    <div class=\"error\" *ngIf=\"errorMessage\">{{errorMessage}}</div>",
        }), 
        __metadata('design:paramtypes', [image_service_1.ImageService])
    ], ImagesListComponent);
    return ImagesListComponent;
}());
exports.ImagesListComponent = ImagesListComponent;
//# sourceMappingURL=images-list.componenet.js.map