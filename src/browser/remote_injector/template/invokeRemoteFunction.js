function invokeRemoteFunction(func, args = null, kwargs = null) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://localhost:{{port}}/invoke/" + func, false);
    xhr.setRequestHeader("Accept", "application/json");
    xhr.setRequestHeader("Content-Type", "application/json");
    let body = {};
    if (args) {
        body["args"] = args;
    }
    if (kwargs) {
        body["kwargs"] = kwargs;
    }
    xhr.send(JSON.stringify(body));

    if (xhr.status >= 200 && xhr.status < 300) {
        const result = JSON.parse(xhr.responseText);
        if (result.status == "success") {
            return result;
        } else if (result.status == "fail") {
            throw new Error(result.detail);
        } else {
            throw new Error("Unknown status")
        }
    } else {
        throw new Error("Request failed with status " + xhr.status);
    }
}
globalThis.invokeRemoteFunction = invokeRemoteFunction;