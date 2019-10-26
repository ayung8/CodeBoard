Webcam.set({
    width: 320,
    height: 240,
    image_format: 'jpeg',
    jpeg_quality: 90
});

function setup() {
    Webcam.reset();
    Webcam.attach( '#my_camera' );
}

function take_snapshot() {
    let img = '';
    Webcam.snap( function(data_uri) {
        document.getElementById('results').innerHTML = 
            '<h2>Here is your image:</h2>' + 
            '<img src="'+data_uri+'"/>';
        img = data_uri.substr(data_uri.indexOf(',') + 1, data_uri.length);
    } );
    Webcam.reset();
    let url = "https://vision.googleapis.com/v1/images:annotate";
    let data = {
        "requests": [
            {
                "image": {
                    "content": img
                },
                "features": [
                    {
                        "type": "TEXT_DETECTION"
                    }
                ]
            }
        ]
    }
    $.get("/runOCR", {"data": JSON.stringify(data)});
}