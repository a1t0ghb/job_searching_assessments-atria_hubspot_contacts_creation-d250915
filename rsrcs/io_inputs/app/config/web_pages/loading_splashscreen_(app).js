//  VARIABLES DECLARATION.
//  'conts' vs. 'let' vs. 'var': 'https://www.freecodecamp.org/news/var-let-and-const-whats-the-difference/'.
const HTML_LOADING = document.getElementById('dialog_loading');

//  CODE EXECUTION.

//  Add an event listener to browser's window: 'https://stackoverflow.com/questions/43558169/addeventlistener-as-a-global-function/43558191#43558191', 'https://www.w3schools.com/jsref/obj_window.asp'.
addEventListener('py:ready', () => HTML_LOADING.close());           //  When loading python script is ready, close HTML_LOADING element: 'https://www.w3schools.com/jsreF/met_dialog_close.asp'.
HTML_LOADING.showModal();                                           //  Show 'modal' dialog; i.e. dialog that locks user interactivity: 'https://www.w3schools.com/jsreF/met_dialog_showModal.asp', 'https://dev.to/iam_timsmith/dialogs-vs-modals-is-there-a-difference-210k'.
