const Dialog = require("dijit/Dialog");

export function test() {
    const dlg = new Dialog({
        content: "Test"
    });
    dlg.show();
}

