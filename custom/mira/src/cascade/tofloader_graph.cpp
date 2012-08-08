// *****************************************************************************
// NICOS, the Networked Instrument Control System of the FRM-II
// Copyright (c) 2009-2012 by the NICOS contributors (see AUTHORS)
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
// Module authors:
//   Tobias Weber <tweber@frm2.tum.de>
//
// *****************************************************************************

TmpGraph::TmpGraph(const TofConfig* pTofConf) :
			m_iW(0), m_puiDaten(0)
{
	if(pTofConf)
		m_TofConfig = *pTofConf;
	else
		m_TofConfig = GlobalConfig::GetTofConfig();
}

TmpGraph::~TmpGraph()
{
	if(m_puiDaten)
	{
		gc.release(m_puiDaten);
		m_puiDaten=NULL;
	}
}

TmpGraph::TmpGraph(const TmpGraph& tmp)
{
	operator=(const_cast<TmpGraph&>(tmp));
}

TmpGraph& TmpGraph::operator=(const TmpGraph& tmp)
{
	m_iW = tmp.m_iW;
	m_puiDaten = tmp.m_puiDaten;
	m_TofConfig = tmp.m_TofConfig;
	gc.acquire(m_puiDaten);

	return *this;
}

unsigned int TmpGraph::GetData(int iX) const
{
	if(!m_puiDaten) return 0;
	if(iX>=0 && iX<m_iW)
		return m_puiDaten[iX];
	return 0;
}

int TmpGraph::GetWidth(void) const { return m_iW; }

int TmpGraph::GetMin() const
{
	if(!m_puiDaten) return 0;

	unsigned int uiMin = std::numeric_limits<int>::max();
	for(int i=0; i<m_iW; ++i)
		if(m_puiDaten[i]<uiMin) uiMin = m_puiDaten[i];
	return uiMin;
}

int TmpGraph::GetMax() const
{
	if(!m_puiDaten) return 0;

	unsigned int uiMax = 0;
	for(int i=0; i<m_iW; ++i)
		if(m_puiDaten[i]>uiMax) uiMax = m_puiDaten[i];
	return uiMax;
}

bool TmpGraph::IsLowerThan(int iTotal) const
{
	int iSum=0;
	for(int i=0; i<m_iW; ++i)
		iSum += GetData(i);

	return iSum < iTotal;
}

bool TmpGraph::FitSinus(double &dFreq, double &dPhase, double &dAmp, double &dOffs,
						double &dPhase_err, double &dAmp_err, double &dOffs_err) const
{
	if(m_iW<=0) return false;
	double dNumOsc = m_TofConfig.GetNumOscillations();

	// Freq fix
	dFreq = dNumOsc * 2.*M_PI/double(m_iW);

	if(IsLowerThan(1))
		return false;

	return ::FitSinus(m_iW, m_puiDaten, dFreq,
					  dPhase, dAmp, dOffs,
					  dPhase_err, dAmp_err, dOffs_err);
}

bool TmpGraph::FitSinus(double& dFreq, double &dPhase, double &dAmp, double &dOffs) const
{
	double dPhase_err, dAmp_err, dOffs_err;

	return FitSinus(dFreq, dPhase, dAmp, dOffs,
					dPhase_err, dAmp_err, dOffs_err);
}

bool TmpGraph::GetContrast(double &dContrast, double &dPhase,
							double &dContrast_err, double &dPhase_err) const
{
	double dFreq;
	double dAmp, dOffs;
	double dAmp_err, dOffs_err;

	if(!FitSinus(dFreq, dPhase, dAmp, dOffs, dPhase_err, dAmp_err, dOffs_err))
		return false;

	dContrast = dAmp / dOffs;
	dContrast_err = sqrt((1/dOffs*dAmp_err)*(1/dOffs*dAmp_err)
					+ (-dAmp/(dOffs*dOffs)*dOffs_err)*(-dAmp/(dOffs*dOffs)*dOffs_err));

	if(dContrast!=dContrast)
		return false;

	return true;
}

bool TmpGraph::GetContrast(double &dContrast, double &dPhase) const
{
	double dContrast_err, dPhase_err;
	return GetContrast(dContrast, dPhase, dContrast_err, dPhase_err);
}

unsigned int TmpGraph::Sum(void) const
{
	unsigned int uiSum = 0;

	for(int i=0; i<m_iW; ++i)
		uiSum += GetData(i);

	return uiSum;
}

bool TmpGraph::Save(const char* pcFile) const
{
	std::ofstream ofstr(pcFile);
	if(!ofstr.is_open())
		return false;

	for(int i=0; i<m_iW; ++i)
	{
		ofstr << i << "\t" << m_puiDaten[i];
		ofstr << "\n";
	}

	ofstr.close();
}
