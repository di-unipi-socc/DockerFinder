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
var software_1 = require('../models/software');
// import {ImagesComponent}  from '../components/images.component'
var router_1 = require("@angular/router");
var ImagesSearchComponent = (function () {
    //
    function ImagesSearchComponent(imageService, router) {
        this.imageService = imageService;
        this.router = router;
        this.sorting = [{ name: 'Ascending stars', val: "stars" }, { name: 'Descending stars', val: "-stars" },
            { name: 'Ascending pulls', val: "pulls" }, { name: 'Descending pulls', val: "-pulls" },
            { name: 'Ascending stars  Ascending pulls', val: "-stars -pulls" }
        ];
        this.comparisons = [{ name: "Greater than", val: "_gt" }, { name: "Less than", val: "_lt" }, { name: "Equal", val: "" }];
        this.softwares = [new software_1.Software("", "", false)]; //{software:'', version:'', error:false}];
        this.msg = '';
        this.selectedSort = { name: "sort", val: "" };
        this.sizeCmpValue = { name: "size", cmp: this.comparisons[0].val, val: "0" }; //size_gt=x, size_lt=y, size=z
        this.pullsCmpValue = { name: "pulls", cmp: this.comparisons[0].val, val: "0" };
        this.starsCmpValue = { name: "stars", cmp: this.comparisons[0].val, val: "0" };
        this.availableSoftware = ["java", "python", "pip", "wget"];
        this.count = 0;
        // private softwareService: SoftwareService){
        //      //this.softwares.push(new Software("", ""));
        //       this.selectedSort.val = this.sorting[0].val;
    }
    ImagesSearchComponent.prototype.ngOnInit = function () {
        //availableSoftwre
    };
    ImagesSearchComponent.prototype.remove = function (id) {
        this.softwares.splice(id, 1);
    };
    ImagesSearchComponent.prototype.add = function (id) {
        this.softwares.push(new software_1.Software(" ", " ", false));
    };
    ImagesSearchComponent.prototype.change_version = function (item) {
        var regex = /^[1-9].([1-9].)*[1-9]$/g;
        if (!regex.test(item.version)) {
            this.msg = "The version syntax it is not correct!";
            item.error = true;
        }
        else {
            this.msg = '';
            item.error = false;
        }
    };
    ImagesSearchComponent.prototype.diagnostic = function () {
        return this.constructSearchUrl();
    };
    ImagesSearchComponent.prototype.onSubmit = function () {
        // //this.constructSearchUrl();
        // this.imageService.searchImages(this.constructSearchUrl())
        //     .then(images=>{
        //          if(images.length > 0 ) {
        //             this.resultImages = images;
        //             this.count = images.length;
        //             console.log(images);
        //         }
        //     });   //res in the json
        var link = ['/images', this.constructSearchUrl()];
        this.router.navigate(link);
    };
    ImagesSearchComponent.prototype.constructSearchUrl = function () {
        var url_search = "";
        for (var _i = 0, _a = this.softwares; _i < _a.length; _i++) {
            var sw = _a[_i];
            url_search += sw.name + "=" + sw.version + "&";
        }
        url_search += "sort=" + this.selectedSort.val;
        url_search += "&" + this.sizeCmpValue.name + this.sizeCmpValue.cmp + "=" + this.sizeCmpValue.val;
        url_search += "&" + this.pullsCmpValue.name + this.pullsCmpValue.cmp + "=" + this.pullsCmpValue.val;
        url_search += "&" + this.starsCmpValue.name + this.starsCmpValue.cmp + "=" + this.starsCmpValue.val;
        return url_search;
    };
    ImagesSearchComponent = __decorate([
        core_1.Component({
            selector: 'my-search-images',
            templateUrl: 'app/template/images-search.component.html',
        }), 
        __metadata('design:paramtypes', [image_service_1.ImageService, router_1.Router])
    ], ImagesSearchComponent);
    return ImagesSearchComponent;
}());
exports.ImagesSearchComponent = ImagesSearchComponent;
//# sourceMappingURL=images-search.component.js.map