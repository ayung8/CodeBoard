Webcam.set({
    width: 480,
    height: 360,
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
    $.post("/runOCR", {"data": JSON.stringify(data)}, function(data) {
        document.getElementById('returnedText').value = data;
    });
}