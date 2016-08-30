/**
 * Created by dido on 7/6/16.
 *
 * Software class represented the name and the version of the software to searching.
 */
export class Software{

    constructor(
        public name:  string,
        public version: string,
        public error : boolean
    ){}
}