/**
 * Created by dido on 7/6/16.
 */

    
export class Image {
    _id: string;
    name:string;
    distro: string;
    last_scan: string;
    description: string;
    full_size: number;
    repo_name: string;
    star_count: number;
    last_updated: string;
    pull_count: number;
    __v : number;
    bins: [ {bin:string, ver: string} ];
}