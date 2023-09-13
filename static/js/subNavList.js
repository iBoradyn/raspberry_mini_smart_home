document.addEventListener('DOMContentLoaded', () => {
    const navItemsCollapseIcon = document.querySelector('.sub-items-collapse-icon');

    if(navItemsCollapseIcon) {
        setSubNavListsHeights();

        navItemsCollapseIcon.addEventListener('click', (e) => {
            toggleSubNavList(e.currentTarget);
        });

        showActiveSidebarSubLink();
        expandActiveLinkSubList();
    }
});

const setSubNavListsHeights = () => {
    const subNavLists = document.querySelectorAll('.sub-nav-list');

    subNavLists.forEach((elem) => {
        elem.style.transition = 'None';
        elem.style.maxHeight = 'None';
        elem.dataset.height = `${elem.offsetHeight}px`;
        elem.style.maxHeight = null;
        elem.style.transition = null;
    });
}

const showSubNavList = (icon, subNavList, animation) => {
    const height = subNavList.dataset.height;

    subNavList.style.borderTop = '1px dashed #000';
    subNavList.style.maxHeight = height;

    if(animation) {
        icon.classList.remove('rotate-down');
        icon.classList.remove('rotate-down-no-animation');
        icon.classList.add('rotate-up');
    } else {
        icon.classList.remove('rotate-down');
        icon.classList.remove('rotate-down-no-animation');
        icon.classList.add('rotate-up-no-animation');
    }
}

const closeSubNavList = (icon, subNavList, animation) => {
    subNavList.style.maxHeight = null;

    if(animation) {
        icon.classList.remove('rotate-up');
        icon.classList.remove('rotate-up-no-animation');
        icon.classList.add('rotate-down');
    } else {
        icon.classList.remove('rotate-up');
        icon.classList.remove('rotate-up-no-animation');
        icon.classList.add('rotate-down-no-animation');
    }

    setTimeout(() => {
        subNavList.style.borderTop = 'None';
    }, 200);
}

const toggleSubNavList = (navList, animation=true) => {
    const icon = navList.children[0];
    const subNavList = navList.parentElement.nextElementSibling;

    if(subNavList.style.maxHeight){
        closeSubNavList(icon, subNavList, animation);
    } else {
        showSubNavList(icon, subNavList, animation);
    }
}

const expandActiveLinkSubList = () => {
    const navLink = document.querySelector('.nav-link.active');

    if(navLink && navLink.parentElement.classList.contains('dropdown')) {
        const icon = navLink.nextElementSibling;

        toggleSubNavList(icon, false);
    }
}

const showActiveSidebarSubLink = () => {
    const subNavSelector = document.querySelector('#active_sub_nav_link_selector').innerHTML.trim().split(',');

    if (subNavSelector[0]) {
        const navLink = document.querySelector(`#${subNavSelector[0]} .sub-item:nth-child(${subNavSelector[1]}) .sub-link`);

        navLink.parentElement.parentElement.previousElementSibling.querySelector('.nav-link').classList.add('sub-active');
        navLink.classList.add('active');
        navLink.setAttribute('aria-current', 'page');

        const icon = navLink.parentElement.parentElement.previousElementSibling.querySelector('.sub-items-collapse-icon');

        toggleSubNavList(icon, false);
    }
}