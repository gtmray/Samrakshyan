import '../../styles/globals.css';
import Navbar from '../components/shared/navbar'
import Router from 'next/router';
import Script from 'next/script';
import nProgress from 'nprogress';
function MyApp({ Component, pageProps }) {
  Router.events.on('routeChangeStart', () => {
    nProgress.start();
  });
  Router.events.on('routeChangeComplete', () => {
    nProgress.done();
  });
  return (
  <div>
    <Navbar/>
    <Component {...pageProps} />
    </div>
    )
}

MyApp.getInitialProps = async ({ Component, ctx }) => {
  let pageProps = {};
  if (Component.getInitialProps) {
    pageProps = await Component.getInitialProps(ctx);
  }
  return { pageProps };
};
export default MyApp;
