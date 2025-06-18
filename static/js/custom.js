document.addEventListener('DOMContentLoaded', function () {
    // 監聽 Modal 顯示事件
    document.addEventListener('show.bs.modal', function (event) {
        setTimeout(function () {
            const backdrop = document.querySelector('.modal-backdrop');
            if (backdrop) {
                backdrop.classList.add('custom-bg');
            }
        }, 0);
    });

    // 監聽 Modal 關閉事件，清理自訂類
    document.addEventListener('hidden.bs.modal', function (event) {
        const backdrop = document.querySelector('.modal-backdrop');
        if (backdrop) {
            backdrop.classList.remove('custom-bg');
        }
    });

    // 確保 AJAX 更新後重新綁定事件
    function bindModalEvents(modalId) {
        const modalElement = document.getElementById(modalId);
        if (modalElement) {
            const modal = bootstrap.Modal.getOrCreateInstance(modalElement);
            modalElement.addEventListener('show.bs.modal', function () {
                const backdrop = document.querySelector('.modal-backdrop');
                if (backdrop) {
                    backdrop.classList.add('custom-bg');
                }
            });
        }
    }

    // 初始綁定
    bindModalEvents('loginModal');
    bindModalEvents('registerModal');
});