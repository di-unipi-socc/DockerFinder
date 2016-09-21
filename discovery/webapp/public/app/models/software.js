"use strict";
/**
 * Created by dido on 7/6/16.
 *
 * Software class represented the name and the version of the software to searching.
 */
var Software = (function () {
    function Software(name, version, error) {
        this.name = name;
        this.version = version;
        this.error = error;
    }
    return Software;
}());
exports.Software = Software;
//# sourceMappingURL=software.js.map