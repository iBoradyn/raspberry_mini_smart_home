document.addEventListener('DOMContentLoaded', () => {
    const sidebarCollapseIcon = document.querySelector('#header_collapse_icon i');

    if(sidebarCollapseIcon) {
        sidebarCollapseIcon.addEventListener('click', toggleSidebarPop);

        showActiveSidebarLink();
    }
});

const toggleSidebarPop = () => {
    document.querySelector('.side-header').classList.toggle('header-pop');
}

const showActiveSidebarLink = () => {
    const navNumber = document.querySelector('#active_nav_link_number').innerHTML;

    if (navNumber) {
        const navLink = document.querySelector(`.nav-list .nav-item:nth-child(${navNumber}) .nav-link`);
        navLink.classList.add('active');
        navLink.setAttribute('aria-current', 'page');
    }
}