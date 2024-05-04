function addComment(product_id) {
    fetch(`/api/products/${product_id}/comments`, {
        method: 'POST',
        body: JSON.stringify({
            content: document.querySelector('#content').value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(c => {
        let m = document.querySelector('#comments');
        m.innerHTML = `
            <li class="list-group-item mb-3">
                <div class="row align-items-center">
                    <div class="col-md-1 col-2">
                        <img class="img-fluid rounded-circle" src="${c.user.avatar}" alt="user-comment"/>
                    </div>
                    <div class="col-md-11 col-10">
                        <p>${c.content}</p>
                        <p class="text-muted">${c.created_date}</p>
                    </div>
                </div>
            </li>
        ` + m.innerHTML;
    })
}