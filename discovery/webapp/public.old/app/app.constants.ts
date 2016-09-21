/**
 * Created by dido on 7/11/16.
 */
import { Injectable } from '@angular/core';

@Injectable()
export class Configuration {
    // public Server: string = "http://127.0.0.1:8000/";
    public ApiUrl: string = "api/images";
    public ServerWithApiUrl = this.ApiUrl;

    constructor(){
    }
}