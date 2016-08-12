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
 * Created by dido on 7/6/16.
 */
var core_1 = require('@angular/core');
var router_1 = require('@angular/router');
var image_service_1 = require("../services/image.service");
var ImagesComponent = (function () {
    function ImagesComponent(router, imageService) {
        this.router = router;
        this.imageService = imageService;
    }
    ImagesComponent.prototype.ngOnInit = function () {
        // this.getImages();
        //this.images =[]
    };
    //
    // getImages() {
    //     this.imageService.getImages().then(images => this.images = images)
    // }
    ImagesComponent.prototype.onSelect = function (image) {
        this.selectedImage = image;
    };
    ImagesComponent.prototype.gotoDetail = function () {
        this.router.navigate(['/detail', this.selectedImage._id]);
    };
    __decorate([
        core_1.Input(), 
        __metadata('design:type', Array)
    ], ImagesComponent.prototype, "images", void 0);
    ImagesComponent = __decorate([
        core_1.Component({
            selector: 'my-images',
            template: "\n    <h1>DoFinder Images</h1>\n     <div *ngIf=\"images && images.length > 0\">\n       <p> Found images : {{images.length}} </p>\n        <ul class=\"images\">\n            <li *ngFor=\"let image of images\"  [class.selected]=\"image === selectedImage\" (click)=\"onSelect(image)\"> \n               <span class=\"badge\"> {{image.stars}}</span> {{image.repo_name}}\n            </li>\n        </ul>\n        <div *ngIf=\"selectedImage\">\n          <h2>\n            {{selectedImage.repo_name | uppercase}} : {{selectedImage.description}}\n          </h2>\n          <button (click)=\"gotoDetail()\">View Details</button>\n        </div>\n    </div>\n    <div *ngIf=\"images && images.length == 0\">\n        Images not found\n    </div>\n    ",
            styleUrls: ['app/styles/images.component.css'],
        }), 
        __metadata('design:paramtypes', [router_1.Router, image_service_1.ImageService])
    ], ImagesComponent);
    return ImagesComponent;
}());
exports.ImagesComponent = ImagesComponent;
//# sourceMappingURL=images.component.js.map