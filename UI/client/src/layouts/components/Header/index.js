import classNames from 'classnames/bind';
import styles from './Header.module.scss';

// import config from './config';

const cx = classNames.bind(styles);

function Header() {
    return (
        <div className={cx("header")}>
            <div className={cx("left-content")}>
                <img src="https://www.fit.hcmus.edu.vn/assets/img/logos/fit-logo.png" alt="AIC Logo" />
                <span>AIC 2023</span>
            </div>
            <div className={cx("right-content")}>
                <span>PTQ.US</span>
            </div>
        </div>
    );
}

export default Header;
