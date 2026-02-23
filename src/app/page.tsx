"use client";

import { useEffect, useState, useRef } from "react";
import * as htmlToImage from 'html-to-image';

interface ParipathData {
  dateStr: string;
  dayStr: string;
  suvichar: { quote: string; author: string };
  mhan: { m: string; a: string };
  english: { e: string; m: string; s1: string; s2: string };
  kode: { q: string; a: string };
  vinod: string;
  gk: string;
  bodhkatha: string;
  dinvishesh: string;
}

export default function Home() {
  const [date, setDate] = useState("");
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState(false);
  const [data, setData] = useState<ParipathData | null>(null);

  const boardRef = useRef<HTMLDivElement>(null);

  // Set initial date to today
  useEffect(() => {
    const today = new Date().toISOString().split("T")[0];
    setDate(today);
  }, []);

  // Fetch data when date changes
  useEffect(() => {
    if (!date) return;

    setLoading(true);
    fetch(`/api/paripath?date=${date}`)
      .then((res) => res.json())
      .then((json: ParipathData) => {
        setData(json);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch paripath data:", err);
        setLoading(false);
      });
  }, [date]);

  const downloadImage = async () => {
    if (!boardRef.current) return;
    setDownloading(true);

    try {
      const board = boardRef.current;

      // Temporarily stash the transform to prevent offset cropping
      const originalTransform = board.style.transform;
      board.style.transform = 'none';

      // 2x scale for HD quality
      const scale = 2;
      const dataUrl = await htmlToImage.toPng(board, {
        quality: 1,
        backgroundColor: '#fffaf0',
        width: board.offsetWidth * scale,
        height: board.offsetHeight * scale,
        style: {
          transform: `scale(${scale})`,
          transformOrigin: 'top left',
          width: `${board.offsetWidth}px`,
          height: `${board.offsetHeight}px`
        }
      });

      // Restore the board scaling
      board.style.transform = originalTransform;

      const a = document.createElement("a");
      a.href = dataUrl;
      a.download = `Paripath_${date}_HD.png`;
      a.click();
    } catch (err) {
      console.error("html-to-image error:", err);
      alert("इमेज तयार करताना काही अडचण आली. कृपया पुन्हा प्रयत्न करा.");
    } finally {
      setDownloading(false);
    }
  };

  return (
    <main>
      {/* Control Panel */}
      <div className="control-panel">
        <label htmlFor="datePicker" className="text-lg font-bold text-gray-700">
          तारीख निवडा (Date):
        </label>
        <input
          type="date"
          id="datePicker"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          className="border-2 border-blue-400 p-2 rounded-lg text-lg font-medium outline-none focus:border-blue-600"
        />
        <span className="text-gray-500 text-sm ml-2 hidden sm:inline">
          (तारीख निवडताच परिपाठ आपोआप तयार होईल)
        </span>
      </div>

      {/* Download Button */}
      <div className="action-buttons">
        <button
          onClick={downloadImage}
          disabled={downloading || loading}
          className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-bold py-3 px-6 rounded-full shadow-lg text-lg flex items-center gap-2"
        >
          {downloading ? (
            <>
              <i className="fas fa-spinner fa-spin"></i> डाऊनलोड होत आहे...
            </>
          ) : (
            <>
              <i className="fas fa-download"></i> डाऊनलोड करा
            </>
          )}
        </button>
      </div>

      {/* Main Board */}
      <div
        ref={boardRef}
        className="paripath-board relative mt-4 mx-auto"
      >
        <div className="bg-shapes"></div>

        {/* Header */}
        <div className="text-center mb-8 relative z-10 flex flex-col items-center justify-center">
          <div className="flex items-center justify-center gap-4 mb-2">
            <i
              className="fas fa-sun text-yellow-500 text-4xl animate-[spin_10s_linear_infinite]"
            ></i>
            <h1
              className="baloo-font title-text font-extrabold m-0"
              contentEditable
              suppressContentEditableWarning
            >
              आजचा परिपाठ
            </h1>
            <i className="fas fa-book-open text-blue-500 text-4xl"></i>
          </div>
          <p
            className="text-2xl text-red-700 font-extrabold bg-white px-8 py-2 rounded-full shadow-md border-2 border-red-200 mt-2"
            contentEditable
            suppressContentEditableWarning
          >
            जिल्हा परिषद प्राथ. शाळा, पाडळदे
          </p>
        </div>

        <div className="grid grid-cols-12 gap-6 relative z-10">
          {/* Left Column */}
          <div className="col-span-12 md:col-span-5 flex flex-col gap-6">
            {/* Date & Day */}
            <div className="section-box box-bg-panchang mt-4">
              <div className="section-header header-bg-panchang baloo-font text-lg">
                <i className="far fa-calendar-alt"></i> दिनांक व वार{" "}
                <i className="fas fa-sun text-yellow-200"></i>
              </div>
              <div
                className="mt-4 text-gray-800 space-y-4 font-medium leading-relaxed text-xl"
                contentEditable
                suppressContentEditableWarning
              >
                <p>
                  <strong>दिनांक :</strong> {data?.dateStr || "लोड होत आहे..."}
                </p>
                <p>
                  <strong>वार :</strong> {data?.dayStr || "..."}
                </p>
              </div>
            </div>

            {/* Dinvishesh */}
            <div className="section-box box-bg-dinvishesh mt-4 flex-grow">
              <div className="section-header header-bg-dinvishesh baloo-font text-lg">
                <i className="fas fa-history"></i> दिनविशेष
              </div>
              <div
                className="mt-4 text-gray-800 text-[15px] space-y-2 leading-tight"
                contentEditable
                suppressContentEditableWarning
                dangerouslySetInnerHTML={{
                  __html: data?.dinvishesh || "<p>लोड होत आहे...</p>",
                }}
              />
            </div>

            {/* Marathi Vinod */}
            <div className="section-box box-bg-vinod mt-4">
              <div className="section-header header-bg-vinod baloo-font text-lg">
                <i className="far fa-laugh-squint"></i> मराठी विनोद
              </div>
              <div
                className="mt-4 text-gray-800 text-[15px] leading-relaxed"
                contentEditable
                suppressContentEditableWarning
                dangerouslySetInnerHTML={{
                  __html: data?.vinod || "<p>लोड होत आहे...</p>",
                }}
              />
            </div>
          </div>

          {/* Right Column */}
          <div className="col-span-12 md:col-span-7 flex flex-col gap-6">
            {/* Suvichar */}
            <div className="section-box box-bg-suvichar mt-4">
              <div className="section-header header-bg-suvichar baloo-font text-lg">
                <i className="fas fa-lightbulb"></i> सुविचार
              </div>
              <div
                className="mt-4 text-center px-4"
                contentEditable
                suppressContentEditableWarning
              >
                <p className="text-[1.2rem] text-blue-900 font-bold leading-tight">
                  {data?.suvichar?.quote || "लोड होत आहे..."}
                </p>
                <p className="text-right text-gray-600 mt-2 font-bold">
                  {data?.suvichar?.author || ""}
                </p>
              </div>
            </div>

            {/* Mhan */}
            <div className="section-box box-bg-mhan mt-4">
              <div className="section-header header-bg-mhan baloo-font text-lg">
                <i className="fas fa-comments"></i> म्हण व अर्थ
              </div>
              <div
                className="mt-3 text-gray-800 text-[15px]"
                contentEditable
                suppressContentEditableWarning
              >
                <p>
                  <strong>म्हण :</strong> {data?.mhan?.m || "लोड होत आहे..."}
                </p>
                <p className="mt-1">
                  <strong>अर्थ :</strong> {data?.mhan?.a || ""}
                </p>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              {/* English */}
              <div className="section-box box-bg-english mt-4 mb-0">
                <div className="section-header header-bg-english baloo-font text-[16px] px-2 w-[90%] text-center">
                  <i className="fas fa-language"></i> इंग्रजी शब्द व वाक्य
                </div>
                <div
                  className="mt-4 text-gray-800 text-[14px] leading-tight"
                  contentEditable
                  suppressContentEditableWarning
                >
                  <p>
                    <strong>English Word :</strong> {data?.english?.e} ({data?.english?.m})
                  </p>
                  <p>
                    <strong>मराठी अर्थ :</strong> {data?.english?.m}
                  </p>
                  <p className="mt-2 text-indigo-900 font-bold">
                    Sentence : {data?.english?.s1}
                  </p>
                  <p className="text-gray-600">{data?.english?.s2}</p>
                </div>
              </div>

              {/* Kode */}
              <div className="section-box box-bg-kode mt-4 mb-0 flex flex-col justify-center items-center text-center">
                <div className="section-header header-bg-kode baloo-font text-[16px]">
                  <i className="fas fa-puzzle-piece"></i> मराठी कोडे
                </div>
                <div
                  className="mt-4 w-full"
                  contentEditable
                  suppressContentEditableWarning
                >
                  <p className="text-lg text-pink-700 font-bold leading-tight mt-2">
                    {data?.kode?.q || "लोड होत आहे..."}
                  </p>
                  <p className="mt-4 text-right text-gray-700 font-bold w-full border-t border-pink-200 pt-1">
                    उत्तर : {data?.kode?.a || ""}
                  </p>
                </div>
              </div>
            </div>

            {/* GK */}
            <div className="section-box box-bg-gk mt-4 flex-grow">
              <div className="section-header header-bg-gk baloo-font text-lg">
                <i className="fas fa-question-circle"></i> सामान्य ज्ञान
              </div>
              <div
                className="mt-4 text-gray-800 text-[14px] leading-relaxed"
                contentEditable
                suppressContentEditableWarning
                dangerouslySetInnerHTML={{
                  __html: data?.gk || "<p>लोड होत आहे...</p>",
                }}
              />
            </div>
          </div>
        </div>

        {/* Bodhkatha */}
        <div className="section-box box-bg-bodhkatha mt-8 relative z-10 mx-2">
          <div className="section-header header-bg-bodhkatha baloo-font text-lg">
            <i className="fas fa-book-reader"></i> बोधकथा
          </div>
          <div
            className="mt-4 text-gray-800 text-[15px] leading-relaxed text-justify"
            contentEditable
            suppressContentEditableWarning
            dangerouslySetInnerHTML={{
              __html: data?.bodhkatha || "<p>लोड होत आहे...</p>",
            }}
          />
        </div>
      </div>
    </main>
  );
}
