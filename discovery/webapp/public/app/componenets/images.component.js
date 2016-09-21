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
    function ImagesComponent(imageService, route) {
        this.imageService = imageService;
        this.route = route;
        this.count = 0;
    }
    ImagesComponent.prototype.ngOnInit = function () {
        var _this = this;
        var searchApi;
        console.log(this.route.params);
        this.route.params.forEach(function (params) {
            console.log(params);
            searchApi = params['parm'];
            // let search= +params['id'];
            _this.imageService.searchImages(searchApi)
                .then(function (resImages) {
                if (resImages.length > 0) {
                    _this.images = resImages;
                    _this.count = resImages.length;
                    console.log(resImages);
                }
            });
        });
    };
    //
    // getImages() {
    //     this.imageService.getImages().then(images => this.images = images)
    // }
    ImagesComponent.prototype.onSelect = function (image) {
        this.selectedImage = image;
    };
    ImagesComponent.prototype.gotoDetail = function () {
        //this.router.navigate(['/detail', this.selectedImage._id]);
    };
    ImagesComponent.prototype.goBack = function () {
        window.history.back();
    };
    __decorate([
        core_1.Input(), 
        __metadata('design:type', Array)
    ], ImagesComponent.prototype, "images", void 0);
    ImagesComponent = __decorate([
        core_1.Component({
            selector: 'my-images',
            template: "\n        <button class=\"btn btn-primary\"  (click)=\"goBack()\">Back</button>\n        <div class=\"row\">\n          <div class=\"col-sm-6 col-md-4\" *ngFor=\"let image of images\"  [class.selected]=\"image === selectedImage\" (click)=\"onSelect(image)\">\n            <div class=\"thumbnail\">\n              <div class=\"caption\">\n                <h4 (click)=\"onSelect(image)\">{{image.repo_name}}</h4>\n                <p><span class=\"badge\">{{image.stars}}</span> Stars</p>\n                <p><span class=\"badge\">{{image.pulls}}</span> Pulls</p>\n                <p><span class=\"badge\">{{image.size}}</span> Size</p>\n                 \n                <!--<p><a href=\"#\" class=\"btn btn-primary\" role=\"button\">Button</a> <a href=\"#\" class=\"btn btn-default\" role=\"button\">Button</a></p>-->\n              </div>\n            </div>\n          </div>\n        </div>\n    <!--<h1>DoFinder Images</h1>\n     <div *ngIf=\"images && images.length > 0\">\n       <p> Found images : {{images.length}} </p>\n        <ul class=\"images\">\n            <li *ngFor=\"let image of images\"  [class.selected]=\"image === selectedImage\" (click)=\"onSelect(image)\"> \n               <span class=\"badge\"> {{image.stars}}</span> {{image.repo_name}}\n            </li>\n        </ul>\n        <div *ngIf=\"selectedImage\">\n          <h2>\n            {{selectedImage.repo_name | uppercase}} : {{selectedImage.description}}\n          </h2>\n          <button (click)=\"gotoDetail()\">View Details</button>\n        </div>\n    </div>\n    <div *ngIf=\"images && images.length == 0\">\n        Images not found\n    </div>-->\n    ",
        }), 
        __metadata('design:paramtypes', [image_service_1.ImageService, router_1.ActivatedRoute])
    ], ImagesComponent);
    return ImagesComponent;
}());
exports.ImagesComponent = ImagesComponent;
//# sourceMappingURL=images.component.js.map