function copyLink() {
    const copyBlock = document.querySelector('.js_copy_link');
    if (!copyBlock) {
        return;
    }
    const link = copyBlock.querySelector('.js_link');
    if (!link) {
        return;
    }
    copyBlock.addEventListener('click', e => {
        e.preventDefault();
        navigator.clipboard.writeText(link.textContent).then(
            result => {
                console.log(result);
            },
            error => {
                console.log(error);
                alert('Не удалось скопировать');
            }
        );
    });
}

copyLink();

export {};
