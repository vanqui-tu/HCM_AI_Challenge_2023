import classNames from 'classnames/bind';
import { Outlet } from "react-router-dom";
import Header from '../components/Header';
import styles from '../styles/Layout.module.css';

const cx = classNames.bind(styles);

function DefaultLayout({ children }) {
    return (
        <div className={cx('wrapper')}>
            <Header />

            {/* All the contents go */}
            <Outlet/>
        </div>
    );
}

export default DefaultLayout;
