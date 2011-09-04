// *****************************************************************************
// Module:
//   $Id$
//
// Author:
//   Tobias Weber <tobias.weber@frm2.tum.de>
//   Georg Brandl <georg.brandl@frm2.tum.de>
//
// NICOS-NG, the Networked Instrument Control System of the FRM-II
// Copyright (c) 2009-2011 by the NICOS-NG contributors (see AUTHORS)
//
// This program is free software; you can redistribute it and/or modify it under
// the terms of the GNU General Public License as published by the Free Software
// Foundation; either version 2 of the License, or (at your option) any later
// version.
//
// This program is distributed in the hope that it will be useful, but WITHOUT
// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
// FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
// details.
//
// You should have received a copy of the GNU General Public License along with
// this program; if not, write to the Free Software Foundation, Inc.,
// 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
//
// *****************************************************************************

#ifndef LW_WIDGET_H
#define LW_WIDGET_H

#include <QPrinter>
#include <QPrintDialog>

#include <qwt_color_map.h>
#include <qwt_plot.h>
#include <qwt_plot_layout.h>
#include <qwt_plot_panner.h>
#include <qwt_plot_spectrogram.h>
#include <qwt_plot_zoomer.h>
#include <qwt_scale_widget.h>

#include "lw_data.h"


class LWZoomer : public QwtPlotZoomer
{
  protected:
    const QwtPlotSpectrogram *m_pData;

  public:
    LWZoomer(QwtPlotCanvas *canvas, const QwtPlotSpectrogram *pData);
    virtual ~LWZoomer();

    virtual QwtText trackerText(const QwtDoublePoint &pos) const;
};


class LWPanner : public QwtPlotPanner
{
  protected:

  public:
    LWPanner(QwtPlotCanvas *canvas);
    virtual ~LWPanner();
};


class LWPlot : public QwtPlot
{
    Q_OBJECT

  protected:
    QwtPlotSpectrogram *m_spectro;
    LWZoomer *m_zoomer;
    LWPanner *m_panner;

  public:
    LWPlot(QWidget *parent);
    virtual ~LWPlot();

    void initPlot();
    void deinitPlot();
    
    void changeRange();
    QwtPlotZoomer *getZoomer() { return m_zoomer; }
    QwtPlotPanner *getPanner() { return m_panner; }
    const QwtRasterData *getData() const { return &m_spectro->data(); }

    void setData(QwtRasterData *pData);
    void setColorMap(bool bCyclic);

  public slots:
    void printPlot();
};


class LWWidget : public QWidget
{
    Q_OBJECT
  private:
    bool m_bForceReinit;

  protected:
    LWPlot *m_plot;
    LWData *m_data;

    ///int m_iMode;
    ///int m_iFolie, m_iZeitkanal;
    bool m_log10;

public:
    LWWidget(QWidget *parent = NULL);
    virtual ~LWWidget();

    ///bool isTofLoaded() const;
    ///bool isPadLoaded() const;
    ///void* newPad();
    ///void* newTof(int iCompression = TOF_COMPRESSION_USEGLOBCONFIG);

    void unload();
    void setData(LWData *data);
    
    ///TofImage* GetTof();
    ///Data2D* GetData2d();
    ///PadData* GetPad();
    LWPlot* plot() { return m_plot; }
    ///unsigned int* GetRawData();

    bool isLog10() { return m_log10; }
    ///int foil() const;
    ///int timechannel() const;

    ///int mode();
    ///void setMode(int mode);

  public slots:
    // sum all foils and all time channels
    ///void viewOverview();
    // show single foil
    ///void viewSlides();
    ///void viewPhases();
    ///void viewContrasts();

    ///void viewFoilSums(const bool *pbKanaele);
    ///void viewPhaseSums(const bool *pbFolien);
    ///void viewContrastSums(const bool *pbFolien);

    // dialogs ////////////////////////////
    ///void showCalibrationDlg(int iNumBins);
    ///void showGraphDlg();
    ///void showSumDlg();
    ///////////////////////////////////////

    void setLog10(bool bLog10);
    ///void setFoil(int iFolie);
    ///void setTimechannel(int iKanal);
    
    void updateGraph();
    void updateLabels();

    ///void sumDlgSlot(const bool *pbKanaele, int iMode);

  signals:
    ///void sumDlgSignal(const bool* pbKanaele, int iMode);
};

#endif
