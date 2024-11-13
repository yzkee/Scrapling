import logging

from scrapling.core._types import Union, Optional, Dict
from .toolbelt import Response, generate_convincing_referer, generate_headers

import httpx
from httpx._models import Response as httpxResponse


class StaticEngine:
    def __init__(self, follow_redirects: bool = True, timeout: Optional[Union[int, float]] = None, adaptor_arguments: Dict = None):
        """An engine that utilizes httpx library, check the `Fetcher` class for more documentation.

        :param follow_redirects: As the name says -- if enabled (default), redirects will be followed.
        :param timeout: The time to wait for the request to finish in seconds. The default is 10 seconds.
        :param adaptor_arguments: The arguments that will be passed in the end while creating the final Adaptor's class.
        """
        self.timeout = timeout
        self.follow_redirects = bool(follow_redirects)
        self._extra_headers = generate_headers(browser_mode=False)
        self.adaptor_arguments = adaptor_arguments if adaptor_arguments else {}

    @staticmethod
    def _headers_job(headers: Optional[Dict], url: str, stealth: bool) -> Dict:
        """Adds useragent to headers if it doesn't exist, generates real headers and append it to current headers, and
        finally generates a referer header that looks like if this request came from Google's search of the current URL's domain.

        :param headers: Current headers in the request if the user passed any
        :param url: The Target URL.
        :param stealth: Whether stealth mode is enabled or not.
        :return: A dictionary of the new headers.
        """
        headers = headers or {}

        # Validate headers
        if not headers.get('user-agent') and not headers.get('User-Agent'):
            headers['User-Agent'] = generate_headers(browser_mode=False).get('User-Agent')
            logging.info(f"Can't find useragent in headers so '{headers['User-Agent']}' was used.")

        if stealth:
            extra_headers = generate_headers(browser_mode=False)
            headers.update(extra_headers)
            headers.update({'referer': generate_convincing_referer(url)})

        return headers

    def _prepare_response(self, response: httpxResponse) -> Response:
        """Takes httpx response and generates `Response` object from it.

        :param response: httpx response object
        :return: A Response object with `url`, `text`, `content`, `status`, `reason`, `encoding`, `cookies`, `headers`, `request_headers`, and the `adaptor` class for parsing, of course.
        """
        return Response(
            url=str(response.url),
            text=response.text,
            content=response.content,
            status=response.status_code,
            reason=response.reason_phrase,
            encoding=response.encoding or 'utf-8',
            cookies=dict(response.cookies),
            headers=dict(response.headers),
            request_headers=dict(response.request.headers),
            adaptor_arguments=self.adaptor_arguments
        )

    def get(self, url: str, stealthy_headers: Optional[bool] = True, **kwargs: Dict) -> Response:
        """Make basic HTTP GET request for you but with some added flavors.
        :param url: Target url.
        :param stealthy_headers: If enabled (default), Fetcher will create and add real browser's headers and
            create a referer header as if this request had came from Google's search of this URL's domain.
        :param kwargs: Any additional keyword arguments are passed directly to `httpx.get()` function so check httpx documentation for details.
        :return: A Response object with `url`, `text`, `content`, `status`, `reason`, `encoding`, `cookies`, `headers`, `request_headers`, and the `adaptor` class for parsing, of course.
        """
        headers = self._headers_job(kwargs.get('headers'), url, stealthy_headers)
        request = httpx.get(url=url, headers=headers, follow_redirects=self.follow_redirects, timeout=self.timeout, **kwargs)
        return self._prepare_response(request)

    def post(self, url: str, stealthy_headers: Optional[bool] = True, **kwargs: Dict) -> Response:
        """Make basic HTTP POST request for you but with some added flavors.
        :param url: Target url.
        :param stealthy_headers: If enabled (default), Fetcher will create and add real browser's headers and
            create a referer header as if this request had came from Google's search of this URL's domain.
        :param kwargs: Any additional keyword arguments are passed directly to `httpx.post()` function so check httpx documentation for details.
        :return: A Response object with `url`, `text`, `content`, `status`, `reason`, `encoding`, `cookies`, `headers`, `request_headers`, and the `adaptor` class for parsing, of course.
        """
        headers = self._headers_job(kwargs.get('headers'), url, stealthy_headers)
        request = httpx.post(url=url, headers=headers, follow_redirects=self.follow_redirects, timeout=self.timeout, **kwargs)
        return self._prepare_response(request)

    def delete(self, url: str, stealthy_headers: Optional[bool] = True, **kwargs: Dict) -> Response:
        """Make basic HTTP DELETE request for you but with some added flavors.
        :param url: Target url.
        :param stealthy_headers: If enabled (default), Fetcher will create and add real browser's headers and
            create a referer header as if this request had came from Google's search of this URL's domain.
        :param kwargs: Any additional keyword arguments are passed directly to `httpx.delete()` function so check httpx documentation for details.
        :return: A Response object with `url`, `text`, `content`, `status`, `reason`, `encoding`, `cookies`, `headers`, `request_headers`, and the `adaptor` class for parsing, of course.
        """
        headers = self._headers_job(kwargs.get('headers'), url, stealthy_headers)
        request = httpx.delete(url=url, headers=headers, follow_redirects=self.follow_redirects, timeout=self.timeout, **kwargs)
        return self._prepare_response(request)

    def put(self, url: str, stealthy_headers: Optional[bool] = True, **kwargs: Dict) -> Response:
        """Make basic HTTP PUT request for you but with some added flavors.
        :param url: Target url.
        :param stealthy_headers: If enabled (default), Fetcher will create and add real browser's headers and
            create a referer header as if this request had came from Google's search of this URL's domain.
        :param kwargs: Any additional keyword arguments are passed directly to `httpx.put()` function so check httpx documentation for details.
        :return: A Response object with `url`, `text`, `content`, `status`, `reason`, `encoding`, `cookies`, `headers`, `request_headers`, and the `adaptor` class for parsing, of course.
        """
        headers = self._headers_job(kwargs.get('headers'), url, stealthy_headers)
        request = httpx.put(url=url, headers=headers, follow_redirects=self.follow_redirects, timeout=self.timeout, **kwargs)
        return self._prepare_response(request)