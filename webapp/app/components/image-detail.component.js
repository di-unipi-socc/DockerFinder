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
var image_service_1 = require('../services/image.service');
var ImageDetailComponent = (function () {
    function ImageDetailComponent(imageService, route) {
        this.imageService = imageService;
        this.route = route;
    }
    ImageDetailComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.sub = this.route.params.subscribe(function (params) {
            var id = +params['id'];
            _this.imageService.getImage(id)
                .then(function (image) { return _this.image = image; });
        });
    };
    ImageDetailComponent.prototype.ngOnDestroy = function () {
        this.sub.unsubscribe();
    };
    ImageDetailComponent.prototype.goBack = function () {
        window.history.back();
    };
    ImageDetailComponent = __decorate([
        core_1.Component({
            selector: 'my-image-detail',
            template: "\n    <div *ngIf=\"image\">\n      <h2>{{image.repo_name}} details!</h2>\n      <div><label>id: </label>{{image._id}}</div>\n      <div>\n        <label>name: </label>\n        <input [(ngModel)]=\"image.repo_name\" placeholder=\"name\">\n      </div>\n     </div>\n     <button (click)=\"goBack()\">Back</button>\n     ",
            styleUrls: ['app/styles/image-detail.component.css']
        }), 
        __metadata('design:paramtypes', [image_service_1.ImageService, router_1.ActivatedRoute])
    ], ImageDetailComponent);
    return ImageDetailComponent;
}());
exports.ImageDetailComponent = ImageDetailComponent;
//# sourceMappingURL=image-detail.component.js.map