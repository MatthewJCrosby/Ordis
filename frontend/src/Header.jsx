import React from "react";
import ordisLogo from './assets/OrdisLogo.png';
function Header() {
    return (
        <header>
            <img src={ordisLogo} className="logo" alt="Ordis logo" />
        </header>
    );
}
export default Header;