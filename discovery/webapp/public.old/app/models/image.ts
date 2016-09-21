/**
 * Created by dido on 7/6/16.
 */

    
export class Image {
    _id: string;
    name:string;
    distro: string;
    last_scan: string;
    description: string;
    size: number;
    repo_name: string;
    stars: number;
    last_updated: string;
    pulls: number;
    __v : number;
    bins: [ {bin:string, ver: string} ];
}