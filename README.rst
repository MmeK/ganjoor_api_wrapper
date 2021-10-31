Ganjoor-Api-Wrapper
===================

Provides an easy way to use the Amazing `Ganjoor Web Service <https://github.com/ganjoor/GanjoorService>`_

Example for getting a faal from hafez::

    >>> from ganjoor import Ganjoor
    >>> go = Ganjoor()
    >>> faal = go.hafez_faal()
    >>> print(faal)

    بیا و کشتی ما در شط شراب انداز
    خروش و ولوله در جان شیخ و شاب انداز

    مرا به کشتی باده درافکن ای ساقی
    که گفته اند نکویی کن و در آب انداز

    ز کوی میکده برگشته ام ز راه خطا
    مرا دگر ز کرم با ره صواب انداز

    بیار زان می گلرنگ مشک بو جامی
    شرار رشک و حسد در دل گلاب انداز

    اگر چه مست و خرابم تو نیز لطفی کن
    نظر بر این دل سرگشته خراب انداز

    به نیمشب اگرت آفتاب می باید
    ز روی دختر گلچهر رز نقاب انداز

    مهل که روز وفاتم به خاک بسپارند
    مرا به میکده بر در خم شراب انداز

    ز جور چرخ چو حافظ به جان رسید دلت
    به سوی دیو محن ناوک شهاب انداز



Installation
------------

Install using pip::

    $ pip install ganjoor-api-wrapper

Or using pipenv::

    $ pipenv install ganjoor-api-wrapper

Contribute
----------

- `Issue Tracker <https://github.com/MmeK/ganjoor_api_wrapper/issues>`_
- `Source Code <https://github.com/MmeK/ganjoor_api_wrapper>`_

License
-------

MIT License

Copyright (c) 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
